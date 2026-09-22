# MobileNet Batch Inference Backpack

This optional example continues the MobileNet application introduced in the
TaskVine section. Instead of running one standalone TaskVine program, you will
deploy a complete Floability backpack containing the workflow, software, data,
and compute specifications.

The workflow performs CPU-only MobileNetV2 inference over 24 openly licensed
Wikimedia Commons images. It is a deployment and execution example, not an
image-classification accuracy benchmark.

## Before you begin

Check which Conda environment is active:

```bash
echo "${CONDA_PREFIX:-No Conda environment is active}"
```

The path should end in `/tutorial-env`. If it does not, activate the tutorial
environment using the command for your setup:

### Live tutorial

```bash
source /opt/tutorial/activate.sh
```

### Self-managed

```bash
conda activate tutorial-env
```

## 1. Get the backpack

Clone the backpack from
[Floability Hub](https://github.com/floability-hub/mobilenet-batch-inference):

```bash
mkdir -p ~/tutorial/examples/backpacks
git clone https://github.com/floability-hub/mobilenet-batch-inference.git \
  ~/tutorial/examples/backpacks/mobilenet-batch-inference
cd ~/tutorial/examples/backpacks/mobilenet-batch-inference
```

The initial run downloads the ONNX model and prepares an inference environment,
so allow more time and disk space than the basic matrix exercise.

## 2. Run the stateful notebook

The backpack has multiple eligible workflows, so every Floability command must select an entrypoint explicitly. Start the stateful Function Library notebook with local workers and ask Floability to copy its generated output directory back into the backpack:

```bash
floability run --backpack . \
  --entrypoint mobilenet-serverless-taskvine.ipynb \
  --sync-path outputs
```

Open JupyterLab using the printed URL. If Floability is running on a remote
system, follow the
[SSH tunnel instructions](../first-backpack.md#4-open-jupyterlab).

Open:

```text
workflow/mobilenet-serverless-taskvine.ipynb
```

Run all cells, save the notebook, and stop Floability with `Ctrl-C`. Inspect the
generated files under:

```text
workflow/outputs/
```

The stateful run produces `stateful-serverless-summary.json` and `stateful-serverless-contact-sheet.jpg`.

## 3. Compare the execution modes

The backpack supports three ways to execute the same classification logic:

| Mode | Where inference runs | Model-loading behavior |
| --- | --- | --- |
| `in-process` | In the Python process | Loaded once in that process; no TaskVine worker |
| `python-task` | In ordinary TaskVine PythonTasks | Each microbatch creates its own model session |
| `stateful-serverless` | In TaskVine library functions | A worker-side library can reuse its loaded model session |

After stopping the stateful run, launch the ordinary PythonTask notebook:

```bash
floability run --backpack . \
  --entrypoint mobilenet-python-task.ipynb \
  --sync-path outputs
```

Open `workflow/mobilenet-python-task.ipynb`, run all cells, save the notebook, and stop Floability with `Ctrl-C`. This run produces `python-task-summary.json` and `python-task-contact-sheet.jpg`.

Compare the mode, timing, task metadata, model-load identifiers, and predictions recorded in the two JSON summaries. This small dataset illustrates the execution models, but it is not a performance benchmark.

To try the worker-free mode, execute the Python entrypoint separately:

```bash
floability execute --backpack . \
  --entrypoint mobilenet-batch-inference.py \
  --no-worker \
  --env-vars MOBILENET_EXECUTION_MODE=in-process \
  --sync-path outputs
```

`--no-worker` is required because `in-process` deliberately runs without a
TaskVine worker.

## 4. Run a distributed workflow without a browser

Either notebook can be executed non-interactively. For example, execute the stateful notebook with:

```bash
floability execute --backpack . \
  --entrypoint mobilenet-serverless-taskvine.ipynb \
  --sync-path outputs
```

The backpack also provides a headless Python entrypoint:

```bash
floability execute --backpack . \
  --entrypoint mobilenet-batch-inference.py \
  --sync-path outputs
```

The Python entrypoint defaults to `stateful-serverless`. To select ordinary PythonTask execution, add `--env-vars MOBILENET_EXECUTION_MODE=python-task`.

## How the workflow is organized

```text
validate manifest and checksums
            |
sort images and create deterministic microbatches
            |
execute batches with the selected mode
            |
collect predictions and execution metadata
            |
write JSON summary and contact sheet
```

The image manifest is the workflow's dataset contract. It records a dataset
identifier and version, the expected number of images, deterministic filenames,
and a SHA-256 checksum for every image. The workflow can therefore process a
different number of images without introducing another classification path.

## Backpack breakdown

### `workflow/`

- `mobilenet-serverless-taskvine.ipynb` uses a persistent TaskVine Function Library and Function Calls.
- `mobilenet-python-task.ipynb` uses ordinary TaskVine PythonTasks.
- `mobilenet-batch-inference.py` provides the headless entrypoint and supports `stateful-serverless`, `python-task`, and `in-process` modes.
- `mobilenet_helpers.py` contains model preprocessing, classification, library
  setup, output validation, and contact-sheet helpers.
- `outputs/` receives mode-specific JSON summaries and contact sheets.

Floability-related configuration and TaskVine orchestration remain visible in
the notebook and entrypoint, while reusable inference operations live in the
helper module.

### `software/`

`environment.yml` pins Python, TaskVine, Jupyter, cloudpickle, ONNX Runtime,
NumPy, and Pillow. The same prepared environment supplies the workflow and its
TaskVine workers.

### `data/`

The default `wikimedia_24` profile combines two data strategies:

- the 24 images and their manifest travel inside the backpack; and
- Floability downloads a revision-pinned MobileNetV2 ONNX model and ImageNet
  label file, validating their expected sizes and SHA-256 checksums.

`IMAGE_CREDITS.md` records image attribution and licenses.
`MODEL_PROVENANCE.md` records model sources, revisions, and checksums.

### `compute/`

`compute.yml` requests two to four local or scheduler-submitted workers. Each
worker has one core, 2 GiB of memory, and 4 GiB of disk in the backpack's
default specification.

## What to verify

A successful run should:

- validate all 24 manifest entries;
- classify every image exactly once;
- report the selected execution mode;
- write a mode-specific JSON summary;
- produce a contact sheet; and
- report successful TaskVine calls for either distributed mode.

For more examples, visit [Floability Hub](https://github.com/floability-hub).
