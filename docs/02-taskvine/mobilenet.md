# MobileNet Batch Inference

This exercise classifies four images with MobileNetV2. The same application is
implemented twice so you can compare ordinary TaskVine PythonTasks with
TaskVine's serverless-style Function Calls.

The complete programs are in:

```text
examples/taskvine/mobilenet-batch-inference/
├── mobilenet-python-task.py
├── mobilenet-serverless.py
├── environment.yml
└── images/
```

## What stays the same

Both programs:

- sort the same four local images and divide them into two microbatches;
- create a named TaskVine manager;
- declare the same pinned MobileNet model, labels, and image inputs;
- submit two independent image-classification operations;
- use one core per operation; and
- collect and validate the same predictions.

The programs differ only in how TaskVine executes the inference function and
manages the model state.

| PythonTask version | Serverless version |
| --- | --- |
| Submits `vine.PythonTask` | Installs a Function Library and submits `vine.FunctionCall` |
| Each task starts an ordinary Python process | Calls execute inside a persistent library process |
| Each task loads a new ONNX session | The library loads one ONNX session during initialization |
| Model and labels are inputs to every task | Model and labels are inputs to the library |
| Two batches produce two model-load IDs | Two batches reuse one model-load ID |

## 1. Create the environment

Move to the example directory:

```bash
cd ~/tutorial/examples/taskvine/mobilenet-batch-inference
```

Create and activate its Conda environment:

```bash
conda env create --file environment.yml
conda activate taskvine-mobilenet
```

If you already created it, only activate it:

```bash
conda activate taskvine-mobilenet
```

The environment provides TaskVine and `cloudpickle` for Python task transport,
ONNX Runtime for CPU inference, NumPy for tensor preparation, and Pillow for
image loading and resizing.

## 2. Run the ordinary PythonTask version

In the first terminal, start the manager application:

```bash
python mobilenet-python-task.py
```

The program prints its manager name and waits for workers.

Open a second terminal, activate the same environment, and run the complete
`vine_factory` command printed by the manager. It will look like:

```bash
conda activate taskvine-mobilenet
vine_factory -T local --min-workers=1 --max-workers=1 \
  --cores=1 \
  --manager-name MANAGER_NAME
```

Use the actual manager name printed by the program. The first run may pause
while TaskVine retrieves the pinned 13.3 MiB model and ImageNet label file.
The one-core worker also ensures that the serverless comparison uses one
one-core Function Library instance.

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

The serverless version first creates a Function Library:

```python
library = manager.create_library_from_functions(
    LIBRARY_NAME,
    classify_image_batch,
    library_context_info=[
        initialize_mobilenet_library,
        ["model.onnx", "labels.txt"],
        {},
    ],
)
manager.install_library(library)
```

`initialize_mobilenet_library` loads the model and labels once. The program
then submits image microbatches as lightweight calls:

```python
call = vine.FunctionCall(
    LIBRARY_NAME,
    "classify_image_batch",
    sandbox_image_paths,
    TOP_K,
)
manager.submit(call)
```

A successful run ends with:

```text
MobileNet serverless batch inference complete.
Classified 4 images in 2 batches using 1 shared model load.
```

Both results should print the same model-load ID, demonstrating that the
Function Calls reused persistent state. Stop the factory with `Ctrl-C`.

## Why use a Function Library?

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

- Return to the [TaskVine hands-on exercises](hands-on.md).
- Review the [TaskVine Quickstart](quickstart.md).
- Review [Matrix Multiplication with TaskVine](matrix.md).
- Read the [official TaskVine Function Calls documentation](https://cctools.readthedocs.io/en/stable/taskvine/#serverless-computing-with-taskvine).
