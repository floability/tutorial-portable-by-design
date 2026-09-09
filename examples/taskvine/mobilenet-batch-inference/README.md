# MobileNet Batch Inference

This example classifies four images with MobileNetV2 in two TaskVine
microbatches. It provides two versions of the same application:

| Program | TaskVine interface | Model loading |
| --- | --- | --- |
| `mobilenet-python-task.py` | Ordinary `PythonTask` | Each task loads its own ONNX session. |
| `mobilenet-serverless.py` | Function Library and `FunctionCall` | One persistent library process loads and reuses the ONNX session. |

Both versions use the same four images, batches, model, labels, manager pattern,
file declarations, and result format. This makes the execution mechanism the
important difference.

## Create the environment

```bash
cd ~/tutorial/examples/taskvine/mobilenet-batch-inference
conda env create --file environment.yml
conda activate taskvine-mobilenet
```

If the environment already exists, only activate it:

```bash
conda activate taskvine-mobilenet
```

## Run the PythonTask version

In the first terminal:

```bash
python mobilenet-python-task.py
```

Open a second terminal, activate the same environment, and run the complete
`vine_factory` command printed by the manager. It will look like:

```bash
conda activate taskvine-mobilenet
vine_factory -T local --min-workers=1 --max-workers=1 \
  --cores=1 \
  --manager-name MANAGER_NAME
```

Use the actual manager name printed by the program. A successful run ends with:

```text
MobileNet PythonTask batch inference complete.
Classified 4 images in 2 batches using 2 independent model loads.
```

Return to the factory terminal and press `Ctrl-C`.

## Run the serverless version

Start a fresh manager in the first terminal:

```bash
python mobilenet-serverless.py
```

In the second terminal, run the new `vine_factory` command printed by this
manager. A successful run ends with:

```text
MobileNet serverless batch inference complete.
Classified 4 images in 2 batches using 1 shared model load.
```

The repeated model-load identifier shows that both Function Calls executed in
the same persistent library process. Stop the factory with `Ctrl-C` afterward.

The one-core worker makes this small comparison deterministic: it can host one
one-core Function Library instance, so both calls reuse that instance.

The factory discovers each named manager through the TaskVine catalog, so these
steps require internet access. On the first run, allow additional time for
TaskVine to retrieve the pinned 13.3 MiB MobileNetV2 model and ImageNet labels.

## What to compare

The applications deliberately follow the same progression:

1. Define the worker-side inference operation.
2. Discover and batch four images.
3. Create a named manager.
4. Declare the model, labels, and images.
5. Submit two microbatches.
6. Collect and validate the predictions.

The PythonTask program sends the model and labels to each ordinary task and
initializes a new ONNX session inside that task. The serverless program attaches
the model and labels to a Function Library, initializes its ONNX session once,
and sends only image microbatches in later Function Calls.

## Data and model

The repository contains four resized Wikimedia Commons images for a quick smoke
test. The images are examples, not an accuracy benchmark.

| Local file | Creator | License | Source |
| --- | --- | --- | --- |
| `golden-retriever.jpg` | Janneke Vreugdenhil; derivative by Anka Friedrich | Public domain | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Golden_Retriever_Dukedestiny01_drvd.jpg) |
| `school-bus.jpg` | Atomic Taco | CC BY-SA 2.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:IC_CE_school_bus_(shortened_chassis).jpg) |
| `strawberry.jpg` | Ivar Leidus | CC BY-SA 4.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Garden_strawberry_(Fragaria_%C3%97_ananassa)_single2.jpg) |
| `tabby-cat.jpg` | Alvesgaspar | CC BY-SA 3.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Cat_November_2010-1a.jpg) |

Model provenance:

- [ONNX Model Zoo MobileNetV2](https://huggingface.co/onnxmodelzoo/mobilenetv2-10), Apache-2.0
- Pinned model revision: `02be6d5da12f60afa5b76260fc44f9f715b4cf75`
- Pinned labels revision: `4f43949841cb55a0b98dc8fcd045431ccafd9f96`
