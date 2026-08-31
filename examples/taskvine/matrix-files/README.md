# Data-Parallel Matrix Multiplication

This example extends the basic command task into a file-based workflow. Three independent tasks multiply three pairs of CSV matrices. TaskVine transfers each task's inputs into a private sandbox and returns its declared result file.

## What this example demonstrates

- Declaring a common program and CSV data files.
- Mapping manager-side paths to worker sandbox filenames.
- Declaring and retrieving task output files.
- Submitting several independent tasks.
- Assigning task tags and resource requirements.
- Collecting results in dynamic completion order.

## Files

```text
matrix-files.py       manager program
multiply_csv.py       program executed by each worker task
data/                 three input matrix pairs
outputs/              generated result matrices
environment.yml       standalone Conda environment
```

The `outputs/` directory is created when the example runs and is ignored by Git.

## Run it

The prepared live tutorial environment already contains the required software. For a standalone environment:

```bash
conda env create --file environment.yml
conda activate taskvine-matrix-files
```

In the first terminal, start the manager:

```bash
python matrix-files.py
```

In a second terminal, activate the same environment and run the complete `vine_worker` command printed by the manager. The one-core worker executes the three tasks and exits automatically when the manager disconnects.

After a successful run, inspect the returned files:

```bash
for result in outputs/*.csv; do
  echo "--- $result"
  cat "$result"
done
```

The tasks may complete in any order. That is expected: TaskVine returns each task as soon as its result is available.

## Extend it

Add another pair of compatible CSV matrices to `data/`, then add its label and filenames to `MATRIX_PAIRS` in `matrix-files.py`. Rerun the manager to include the new independent task.
