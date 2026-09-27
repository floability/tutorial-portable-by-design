# MobileNet Batch Inference

This exercise classifies four images with MobileNetV2. The same application is
implemented twice so you can compare ordinary TaskVine PythonTasks with
TaskVine's serverless-style Function Calls.

Run both versions first. A short explanation of the two execution models
follows the exercise for anyone who wants to inspect how they differ.

## Before you begin

Check which Conda environment is active:

```bash
echo "${CONDA_PREFIX:-No Conda environment is active}"
```

The path should end in `/tutorial-env`. If it does not, activate the tutorial
environment using the command for your setup:

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

```bash
source /opt/tutorial/activate.sh
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

```bash
conda activate tutorial-env
```

**Continue with either setup**

## 1. Enter the example directory

Move to the example directory:

```bash
cd ~/tutorial/examples/taskvine/mobilenet-batch-inference
```

The example includes a standalone `environment.yml`, but `tutorial-env` already contains TaskVine, cloudpickle, ONNX Runtime, NumPy, and Pillow. Confirm those imports:

```bash
python -c "import cloudpickle, numpy, onnxruntime; from PIL import Image; import ndcctools.taskvine; print('MobileNet environment: OK')"
```

These packages provide Python task transport, CPU inference, tensor preparation, and image loading and resizing.

## 2. Run the ordinary PythonTask version

In the first terminal, start the manager application:

```bash
python mobilenet-python-task.py
```

The program prints its manager name and waits for workers.

Open a second terminal and activate `tutorial-env` using the command for your setup.

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

```bash
source /opt/tutorial/activate.sh
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

```bash
conda activate tutorial-env
```

**Continue with either setup**

Then copy the complete `vine_factory` command printed by the manager. It will look like:

```bash
vine_factory -T local --min-workers=1 --max-workers=1 \
  --cores=1 \
  --timeout=60 \
  --scratch-dir "$HOME/vine_scratch/<MANAGER_NAME>" \
  --manager-name <MANAGER_NAME>
```

Use the complete command printed by the program. It contains the actual
manager name and a matching run-specific scratch directory. This prevents a
lingering worker from an earlier run from blocking the next factory while it
stages its `vine_worker` executable. The 60-second timeout limits how long an
idle worker can remain after shutdown. The first run may pause while TaskVine
retrieves the pinned 13.3 MiB model and ImageNet label file. The one-core worker
also ensures that the serverless comparison uses one one-core Function Library
instance.

The run should finish with:

```text
MobileNet PythonTask batch inference complete.
Classified 4 images in 2 batches using 2 independent model loads.
```

The two load IDs show that each ordinary PythonTask initialized its own ONNX
session. Return to the factory terminal and press `Ctrl-C`.

## 3. Run the serverless version

In the first terminal, start a fresh manager:

```bash
python mobilenet-serverless.py
```

In the second terminal, run the new `vine_factory` command printed by this
manager. Use the new manager name rather than the name from the previous run.

A successful run ends with:

```text
MobileNet serverless batch inference complete.
Classified 4 images in 2 batches using 1 shared model load.
```

Both results should print the same model-load ID, demonstrating that the
Function Calls reused persistent state. Stop the factory with `Ctrl-C`.

## TL;DR: two ways to run a Python function

Both programs divide the same four images into two microbatches and run the
same classification operation. They differ in what TaskVine starts for each
operation and where the MobileNet model is loaded.

### Ordinary PythonTask

A [`PythonTask`](https://cctools.readthedocs.io/en/stable/taskvine/#python-tasks)
packages a Python function and its arguments as one TaskVine task. Its Python
return value becomes `completed.output`, while normal TaskVine file and
resource controls still apply.

In `mobilenet-python-task.py`, the manager submits one task per microbatch:

```python
task = vine.PythonTask(
    classify_image_batch,
    "model.onnx",
    "labels.txt",
    sandbox_image_paths,
    TOP_K,
)
```

The model and labels are inputs to each task. When a task starts,
`classify_image_batch` creates its own ONNX inference session, classifies two
images, returns the predictions, and exits. Two microbatches therefore create
two independent sessions and print two different model-load IDs.

### Function Library and FunctionCall

A [Function Library](https://cctools.readthedocs.io/en/stable/taskvine/#serverless-computing)
is a persistent task that makes named Python functions available on a worker.
After the manager installs the library, it submits `FunctionCall` tasks that
invoke those functions by name.

In `mobilenet-serverless.py`, making the classification function available
requires five steps.

#### 1. Initialize the shared model state

The initializer receives the model and label filenames, creates the ONNX
session, and returns a dictionary of values that later calls can retrieve:

```python
def initialize_mobilenet_library(model_path, labels_path):
    import uuid
    import onnxruntime as ort

    session = ort.InferenceSession(
        model_path,
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
        "model_load_id": uuid.uuid4().hex[:8],
    }
```

This function runs when the Function Library starts, not once per image
microbatch. The returned dictionary becomes the library's shared state.

#### 2. Define the callable function

The callable accepts only the values that change between calls. It retrieves
the persistent model state by name:

```python
def classify_image_batch(image_paths, top_k):
    from ndcctools.taskvine.utils import load_variable_from_library

    session = load_variable_from_library("inference_session")
    labels = load_variable_from_library("imagenet_labels")
    model_load_id = load_variable_from_library("model_load_id")

    # Preprocess the images and run inference with session.
    predictions = ...

    return {
        "predictions": predictions,
        "model_load_id": model_load_id,
    }
```

The complete function in the example contains the image preprocessing and
inference code represented by `...` above.

#### 3. Create and install the Function Library

The manager packages `classify_image_batch` as a named library function. The
`library_context_info` value identifies the initializer, its positional
arguments, and its keyword arguments:

```python
library = manager.create_library_from_functions(
    LIBRARY_NAME,
    classify_image_batch,
    add_env=False,
    exec_mode="direct",
    library_context_info=[
        initialize_mobilenet_library,
        ["model.onnx", "labels.txt"],
        {},
    ],
)
library.add_input(model_file, "model.onnx")
library.add_input(labels_file, "labels.txt")
library.set_cores(1)
library.set_function_slots(1)
manager.install_library(library)
```

The model and labels are inputs to the library rather than to every call.
Their sandbox names match the filenames passed to the initializer. Direct
execution keeps each call inside the library process, and one function slot
allows that process to handle one microbatch at a time.

Installing the library makes TaskVine dispatch it to an available worker. The
worker starts the library, runs `initialize_mobilenet_library`, and then keeps
the library ready for calls.

#### 4. Submit FunctionCall tasks

Each microbatch becomes a call to the named function in the named library:

```python
call = vine.FunctionCall(
    LIBRARY_NAME,
    "classify_image_batch",
    sandbox_image_paths,
    TOP_K,
)
for image_path, sandbox_path in zip(image_batch, sandbox_image_paths):
    call.add_input(declared_images[image_path], sandbox_path)
call.set_cores(1)
manager.submit(call)
```

Only the images and ordinary function arguments vary between calls. TaskVine
stages each call's images, invokes `classify_image_batch`, and returns its
Python value through `completed.output`, just as it does for a PythonTask.

#### 5. Reuse the initialized state

Both calls retrieve the same ONNX session, labels, and model-load ID from the
persistent library process. The repeated model-load ID in the output is the
visible proof that the initializer ran once and both microbatches reused its
state.

The manager collects each returned Python value through the normal TaskVine
wait loop:

```python
while not manager.empty():
    completed = manager.wait(5)
    if completed:
        result = completed.output
        print(result["model_load_id"])
```

| Ordinary `PythonTask` | Function Library with `FunctionCall` |
| --- | --- |
| One self-contained Python task per microbatch | One persistent library serves multiple calls |
| Model and labels are task inputs | Model and labels are library inputs |
| Creates a new ONNX session for every task | Initializes one ONNX session for the library |
| Simpler for independent, longer-running work | Useful when many short calls share expensive startup state |

Ordinary PythonTasks are direct and work well for independent functions with
little startup cost. For machine-learning inference, repeatedly importing
libraries and loading a model can become a significant part of every task.

A Function Library moves that initialization into a persistent worker-side
process. Later Function Calls carry only their arguments and declared image
inputs. The same pattern applies to scientific libraries, lookup tables, model
weights, and other expensive reusable state.

This four-image exercise demonstrates behavior rather than performance. A
larger workload is needed for a meaningful timing comparison.

## TaskVine hands-on navigation

- Return to the [TaskVine overview and exercises](index.md).
- Review the [TaskVine Quickstart](quickstart.md).
- Review [Matrix Multiplication with TaskVine](matrix.md).
- Read the [official TaskVine Function Calls documentation](https://cctools.readthedocs.io/en/stable/taskvine/#serverless-computing).

[**Next: Sciunit overview →**](../03-sciunit/index.md)
