# Basic Matrix Multiplication

This is the smallest TaskVine example in the tutorial. One manager submits one command task, one local worker performs a fixed 2-by-2 matrix multiplication, and the result returns through the task's standard output. No input or output files are transferred.

## What this example demonstrates

- Creating a TaskVine manager on an available port.
- Defining and submitting one command task.
- Requesting one core for the task.
- Connecting a resource-limited local worker.
- Waiting for a result and checking whether the task succeeded.

## Run it

The prepared live tutorial environment already contains the required software. For a standalone environment, create and activate the included Conda environment:

```bash
conda env create --file environment.yml
conda activate taskvine-matrix-basic
```

In the first terminal, enter this directory and start the manager:

```bash
python matrix-basic.py
```

The manager prints a `vine_worker` command containing its selected port. Leave it running. In a second terminal, activate the same environment and run the complete command that was printed.

The worker uses `--single-shot`, so it exits automatically after the manager disconnects. The manager validates and prints:

```text
Result: [[19, 22], [43, 50]]

Basic matrix multiplication complete.
```

## Read the program

The matrices and the short worker program are embedded in the task command. This keeps the access-validation example independent of external data and introduces command tasks before the next example adds TaskVine file declarations.
