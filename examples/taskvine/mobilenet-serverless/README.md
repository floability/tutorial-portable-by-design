# MobileNet with TaskVine Function Calls

This optional advanced example classifies four images with MobileNetV2. It uses a TaskVine **Function Library** to load the ONNX model once on a worker, followed by four lightweight **Function Calls** that reuse the loaded model.

TaskVine describes this serverless-style model as Function Calls and Function Libraries. It is useful when many tasks repeatedly invoke an expensive scientific or machine-learning function whose initialization state can be reused.

## What this example demonstrates

- Initializing persistent state inside a Function Library.
- Loading one ONNX inference session per library process.
- Submitting one Function Call per image.
- Transferring local images and pinned remote model assets with TaskVine.
- Reusing the same library process across multiple calls.
- Returning structured Python results to the manager.

## Dataset and model

The repository contains four resized Wikimedia Commons images for a quick smoke test. The program declares and retrieves a pinned 13.3 MiB MobileNetV2 model and its ImageNet labels on the first run. Workers receive the declared files through TaskVine rather than downloading them inside inference calls.

Model provenance:

- [ONNX Model Zoo MobileNetV2](https://huggingface.co/onnxmodelzoo/mobilenetv2-10), Apache-2.0
- Pinned model revision: `02be6d5da12f60afa5b76260fc44f9f715b4cf75`
- Pinned labels revision: `4f43949841cb55a0b98dc8fcd045431ccafd9f96`

Image attribution:

| Local file | Creator | License | Source |
| --- | --- | --- | --- |
| `golden-retriever.jpg` | Janneke Vreugdenhil; derivative by Anka Friedrich | Public domain | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Golden_Retriever_Dukedestiny01_drvd.jpg) |
| `school-bus.jpg` | Atomic Taco | CC BY-SA 2.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:IC_CE_school_bus_(shortened_chassis).jpg) |
| `strawberry.jpg` | Ivar Leidus | CC BY-SA 4.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Garden_strawberry_(Fragaria_%C3%97_ananassa)_single2.jpg) |
| `tabby-cat.jpg` | Alvesgaspar | CC BY-SA 3.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Cat_November_2010-1a.jpg) |

## Run it

The prepared live tutorial environment includes the required machine-learning packages. For a standalone environment, create and activate the included Conda environment:

```bash
conda env create --file environment.yml
conda activate taskvine-mobilenet-serverless
```

In the first terminal, start the manager:

```bash
python mobilenet-serverless.py
```

In a second terminal, activate the same environment and run the complete `vine_worker` command printed by the manager. Allow additional time on the first run for TaskVine to retrieve the model.

A successful run prints one classification per image and finishes with output similar to:

```text
MobileNet Function Library example complete.
Four calls reused one model load: LOAD_ID
```

The repeated load identifier is the important observation: all four calls executed against the same model session instead of loading MobileNet separately for every image.

## Follow the program step by step

`mobilenet-serverless.py` is deliberately kept as one teaching script. Its numbered sections show the complete progression:

1. Define the library initializer.
2. Define the reusable classification function.
3. Discover four local images.
4. Create the manager and print the worker command.
5. Declare model, label, and image files.
6. Construct and install the Function Library.
7. Submit one Function Call per image.
8. Collect results and confirm model reuse.

This example is complete but optional during the live session. Participants can return to it after completing the two matrix exercises.
