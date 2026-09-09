#!/usr/bin/env python3
"""Classify four images in two ordinary TaskVine PythonTask microbatches."""

import getpass
import os
from pathlib import Path

import ndcctools.taskvine as vine


EXAMPLE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = EXAMPLE_DIR / "images"
BATCH_SIZE = 2
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


# Step 1: Define an ordinary Python function for one image microbatch.
# PythonTask serializes this function and runs it in a worker sandbox, so its
# imports and image preprocessing are intentionally self-contained.
def classify_image_batch(model_path, labels_path, image_paths, top_k):
    import os
    import socket
    import uuid
    from pathlib import Path

    import numpy as np
    import onnxruntime as ort
    from PIL import Image

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

    predictions = []
    for image_path in image_paths:
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

        predictions.append(
            {
                "image": Path(image_path).name,
                "predictions": [
                    {
                        "label": labels[index],
                        "probability": float(probabilities[index]),
                    }
                    for index in best_indices
                ],
            }
        )

    return {
        "predictions": predictions,
        "model_load_id": uuid.uuid4().hex[:8],
        "worker_hostname": socket.gethostname(),
        "worker_pid": os.getpid(),
    }


def main():
    # Step 2: Discover four images and divide them into deterministic batches.
    image_paths = sorted(
        path
        for path in IMAGE_DIR.iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
    if len(image_paths) != 4:
        raise RuntimeError(
            f"Expected four tutorial images; found {len(image_paths)}"
        )

    image_batches = [
        image_paths[index : index + BATCH_SIZE]
        for index in range(0, len(image_paths), BATCH_SIZE)
    ]

    # Step 3: Create a named manager that vine_factory can discover.
    manager_name = f"mobilenet-batch-{getpass.getuser()}-{os.getpid()}"
    manager = vine.Manager(port=0, name=manager_name)

    print(f"Manager name: {manager_name}")
    print(f"Listening on port: {manager.port}")
    print("\nIn a second terminal, activate the same environment and run:")
    print(
        "vine_factory -T local --min-workers=1 --max-workers=1 "
        "--cores=1 "
        f"--manager-name {manager_name}"
    )

    # Step 4: Declare the model, labels, and local images as TaskVine inputs.
    model_file = manager.declare_url(MODEL_URL, cache="workflow")
    labels_file = manager.declare_url(LABELS_URL, cache="workflow")
    declared_images = {
        image_path: manager.declare_file(str(image_path), cache=True)
        for image_path in image_paths
    }

    # Step 5: Submit one ordinary PythonTask for each image microbatch.
    submitted_batches = {}
    for batch_number, image_batch in enumerate(image_batches, start=1):
        batch_name = f"batch-{batch_number}"
        sandbox_image_paths = [
            f"images/{image_path.name}" for image_path in image_batch
        ]
        task = vine.PythonTask(
            classify_image_batch,
            "model.onnx",
            "labels.txt",
            sandbox_image_paths,
            TOP_K,
        )
        task.add_input(model_file, "model.onnx")
        task.add_input(labels_file, "labels.txt")
        for image_path, sandbox_path in zip(
            image_batch, sandbox_image_paths, strict=True
        ):
            task.add_input(declared_images[image_path], sandbox_path)
        task.set_tag(batch_name)
        task.set_cores(1)

        task_id = manager.submit(task)
        submitted_batches[task_id] = batch_name

    print(f"\nSubmitted {len(submitted_batches)} image microbatches.")
    print("Waiting for workers...")

    # Step 6: Collect completed tasks in their dynamic completion order.
    results = []
    failures = []
    while not manager.empty():
        completed = manager.wait(5)
        if not completed:
            continue

        batch_name = submitted_batches[completed.id]
        if not completed.successful():
            failures.append((batch_name, completed.result))
            print(f"FAILED {batch_name}: TaskVine result={completed.result}")
            continue
        if isinstance(completed.output, Exception):
            failures.append((batch_name, repr(completed.output)))
            print(f"FAILED {batch_name}: {completed.output!r}")
            continue

        result = completed.output
        results.append(result)
        print(
            f"\nCompleted {batch_name} on {completed.addrport}; "
            f"model load={result['model_load_id']}"
        )
        for prediction in result["predictions"]:
            best = prediction["predictions"][0]
            print(
                f"  {prediction['image']:<22} {best['label']:<38} "
                f"{best['probability']:.1%}"
            )

    if failures:
        raise RuntimeError(f"MobileNet inference failures: {failures}")

    classified_images = sum(
        len(result["predictions"]) for result in results
    )
    if classified_images != len(image_paths):
        raise RuntimeError(
            f"Received predictions for {classified_images} of "
            f"{len(image_paths)} images"
        )

    model_load_ids = {result["model_load_id"] for result in results}
    if len(model_load_ids) != len(image_batches):
        raise RuntimeError("Each PythonTask should create its own ONNX session")

    print("\nMobileNet PythonTask batch inference complete.")
    print(
        f"Classified {classified_images} images in {len(results)} batches "
        f"using {len(model_load_ids)} independent model loads."
    )


if __name__ == "__main__":
    main()
