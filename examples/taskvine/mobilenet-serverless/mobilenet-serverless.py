#!/usr/bin/env python3
"""Classify four images with a stateful TaskVine Function Library."""

import getpass
from pathlib import Path

import ndcctools.taskvine as vine


EXAMPLE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = EXAMPLE_DIR / "images"
LIBRARY_NAME = "mobilenet-inference"
TOP_K = 3

MODEL_URL = (
    "https://huggingface.co/onnxmodelzoo/mobilenetv2-10/resolve/"
    "02be6d5da12f60afa5b76260fc44f9f715b4cf75/mobilenetv2-10.onnx"
)
LABELS_URL = (
    "https://raw.githubusercontent.com/onnx/models/"
    "4f43949841cb55a0b98dc8fcd045431ccafd9f96/validated/vision/"
    "classification/synset.txt"
)


# Step 1: Define the function that initializes one persistent library process.
# The ONNX model is loaded once here instead of being reloaded for every image.
def load_mobilenet_library(model_path, labels_path):
    import os
    import socket
    import uuid

    import onnxruntime as ort

    session_options = ort.SessionOptions()
    session_options.intra_op_num_threads = 1
    session_options.inter_op_num_threads = 1
    session = ort.InferenceSession(
        model_path,
        sess_options=session_options,
        providers=["CPUExecutionProvider"],
    )

    with open(labels_path, encoding="utf-8") as labels_file:
        labels = [
            line.strip().split(" ", 1)[1]
            for line in labels_file
            if line.strip()
        ]

    return {
        "inference_session": session,
        "imagenet_labels": labels,
        "library_load_id": uuid.uuid4().hex[:8],
        "library_hostname": socket.gethostname(),
        "library_pid": os.getpid(),
    }


# Step 2: Define the function called once per image. TaskVine supplies access to
# the state created by load_mobilenet_library inside the persistent process.
def classify_image(image_path, top_k):
    import os
    from pathlib import Path

    import numpy as np
    from ndcctools.taskvine.utils import load_variable_from_library
    from PIL import Image

    session = load_variable_from_library("inference_session")
    labels = load_variable_from_library("imagenet_labels")

    with Image.open(image_path) as source_image:
        image = source_image.convert("RGB")
        width, height = image.size
        scale = 256.0 / min(width, height)
        resized = image.resize(
            (round(width * scale), round(height * scale)),
            Image.Resampling.BILINEAR,
        )
        left = (resized.width - 224) // 2
        top = (resized.height - 224) // 2
        cropped = resized.crop((left, top, left + 224, top + 224))

    image_array = np.asarray(cropped, dtype=np.float32) / 255.0
    image_array = (
        image_array - np.array([0.485, 0.456, 0.406], dtype=np.float32)
    ) / np.array([0.229, 0.224, 0.225], dtype=np.float32)
    input_tensor = np.transpose(image_array, (2, 0, 1))[None, ...]

    scores = session.run(
        None,
        {session.get_inputs()[0].name: input_tensor},
    )[0].reshape(-1)
    probabilities = np.exp(scores - np.max(scores))
    probabilities /= probabilities.sum()
    best_indices = np.argsort(probabilities)[-top_k:][::-1]

    return {
        "image": Path(image_path).name,
        "predictions": [
            {
                "label": labels[index],
                "probability": float(probabilities[index]),
            }
            for index in best_indices
        ],
        "library_load_id": load_variable_from_library("library_load_id"),
        "library_hostname": load_variable_from_library("library_hostname"),
        "library_pid": load_variable_from_library("library_pid"),
        "function_pid": os.getpid(),
    }


# Step 3: Discover the small, deterministic smoke-test dataset.
image_paths = sorted(
    path
    for path in IMAGE_DIR.iterdir()
    if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
)
if len(image_paths) != 4:
    raise RuntimeError(f"Expected four tutorial images; found {len(image_paths)}")


# Step 4: Create the manager and print the command for one local worker.
manager_name = f"mobilenet-serverless-{getpass.getuser()}"
manager = vine.Manager(port=0, name=manager_name)
manager.tune("watch-library-logfiles", 1)

print(f"Manager name: {manager_name}")
print(f"Listening on port: {manager.port}")
print("\nIn a second terminal, activate the same environment and run:")
print(
    "vine_worker --single-shot --cores=1 --memory=4096 --disk=4096 "
    f"localhost {manager.port}"
)


# Step 5: Declare pinned remote model assets and local image inputs. TaskVine
# transfers these files to the worker; inference calls do not access the network.
model_file = manager.declare_url(MODEL_URL, cache="workflow")
labels_file = manager.declare_url(LABELS_URL, cache="workflow")
declared_images = {
    image_path: manager.declare_file(str(image_path), cache=True)
    for image_path in image_paths
}


# Step 6: Construct and install the Function Library. Its context function loads
# the model once, while one function slot processes calls sequentially.
library = manager.create_library_from_functions(
    LIBRARY_NAME,
    classify_image,
    add_env=False,
    exec_mode="direct",
    library_context_info=[
        load_mobilenet_library,
        ["model.onnx", "labels.txt"],
        {},
    ],
)
library.add_input(model_file, "model.onnx")
library.add_input(labels_file, "labels.txt")
library.set_cores(1)
library.set_function_slots(1)
manager.install_library(library)
print(f"\nInstalled persistent Function Library: {LIBRARY_NAME}")


# Step 7: Submit one lightweight FunctionCall per image. Each call receives only
# its image and invokes classify_image inside the already-running library.
submitted = {}
for image_path in image_paths:
    call = vine.FunctionCall(
        LIBRARY_NAME,
        "classify_image",
        f"images/{image_path.name}",
        TOP_K,
    )
    call.add_input(declared_images[image_path], f"images/{image_path.name}")
    call.set_tag(image_path.name)
    call.set_cores(1)
    task_id = manager.submit(call)
    submitted[task_id] = image_path.name

print(f"Submitted {len(submitted)} image-classification calls.")
print("Waiting for the worker and the first model load...")


# Step 8: Collect results and verify that every call reused the same library.
results = []
failures = []
while not manager.empty():
    completed = manager.wait(5)
    if not completed:
        continue
    if not completed.successful():
        failures.append((submitted[completed.id], completed.result))
        print(
            f"FAILED {submitted[completed.id]}: "
            f"TaskVine result={completed.result}"
        )
        continue

    result = completed.output
    if result["function_pid"] != result["library_pid"]:
        raise RuntimeError("FunctionCall did not run in its Function Library")
    results.append(result)
    best = result["predictions"][0]
    print(
        f"{result['image']:<22} {best['label']:<38} "
        f"{best['probability']:.1%}  library={result['library_load_id']}"
    )

if failures:
    raise RuntimeError(f"MobileNet inference failures: {failures}")
if len(results) != len(image_paths):
    raise RuntimeError(
        f"Received {len(results)} results for {len(image_paths)} images"
    )

library_load_ids = {result["library_load_id"] for result in results}
if len(library_load_ids) != 1:
    raise RuntimeError(
        f"Expected one persistent model load; observed {library_load_ids}"
    )

print("\nMobileNet Function Library example complete.")
print(f"Four calls reused one model load: {library_load_ids.pop()}")
