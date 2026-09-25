# Matrix Multiplication with TaskVine

The quickstart used `vine.Task` to execute a Linux command. This exercise
introduces `vine.PythonTask`, which executes a Python function with Python
arguments and returns the function's value as `task.output`.

The application multiplies two pairs of matrices stored as CSV files. Each
PythonTask reads declared input files from its worker sandbox and writes a
declared output file for TaskVine to return.

## Before you begin

Complete [Access and Setup](../01-access-and-setup/index.md) before starting.
Both setup routes place the repository at `~/tutorial` and provide the matrix
dependencies in `tutorial-env`.

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

```bash
cd ~/tutorial/examples/taskvine/matrix-files
ls
```

You should see:

```text
README.md  data  environment.yml  matrix-files.py
```

## 2. Check the matrix dependencies

The example includes a standalone `environment.yml`. You do not need to create
another environment during this tutorial because `tutorial-env` already
contains these packages:

```yaml
dependencies:
  - python=3.11
  - ndcctools=7.17.1
  - cloudpickle=3.1.2
  - numpy=2.4.3
```

Each dependency has a purpose:

| Dependency | Purpose |
| --- | --- |
| Python | Runs the manager and the function on workers. |
| TaskVine (`ndcctools`) | Provides the manager, PythonTask, worker, and factory. |
| `cloudpickle` | Serializes the Python function, its arguments, and its return value. |
| NumPy | Reads, multiplies, and writes the CSV matrices. |

A PythonTask serializes Python code and values; it does not automatically
install imported third-party libraries. Because `multiply_matrix_files`
imports NumPy, NumPy must be available in the worker's Python environment.
Starting both the manager and `vine_factory` from `tutorial-env` gives them the
same dependencies.

Confirm the important imports:

```bash
python -c "import cloudpickle, numpy; import ndcctools.taskvine; print('PythonTask environment: OK')"
```

## 3. Start the manager application

In the first terminal, run:

```bash
python matrix-files.py
```

The program creates a manager with a unique project name, submits two tasks,
prints the manager's selected port, and waits:

```text
Manager name: <MANAGER_NAME>
Listening on port: <PORT>
Factory scratch directory: <SCRATCH_DIRECTORY>

In a second terminal, activate this environment and run:
vine_factory ... --scratch-dir <SCRATCH_DIRECTORY> --manager-name <MANAGER_NAME>

Submitted two file-based PythonTasks. Waiting for the factory worker...
```

Leave the manager running.

## 4. Start a local TaskVine factory

Open a second terminal on the same tutorial server or self-managed Linux
system.

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

Connect to your assigned server if necessary, then activate the shared
tutorial environment:

```bash
source /opt/tutorial/activate.sh
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

Activate the tutorial environment:

```bash
conda activate tutorial-env
```

**Continue with either setup**

Copy the complete `vine_factory` command printed by the manager and run it in
the second terminal. It will look like:

```bash
vine_factory -T local --min-workers=1 --max-workers=2 \
  --timeout=60 \
  --scratch-dir "$HOME/vine_scratch/<MANAGER_NAME>" \
  --manager-name <MANAGER_NAME>
```

Use the complete command printed by the program. It contains the actual
manager name and the matching absolute scratch-directory path.

The options have distinct purposes:

| Option | Meaning |
| --- | --- |
| `-T local` | Launch workers as local processes instead of submitting them to an HPC batch system. |
| `--manager-name` | Find the named manager through the TaskVine catalog. |
| `--min-workers=1` | Maintain at least one worker while the manager is active. |
| `--max-workers=2` | Allow the factory to scale up to two workers when tasks are waiting. |
| `--timeout=60` | Stop a worker after 60 seconds without a manager connection or work. |
| `--scratch-dir` | Keep this run's factory files and worker executable separate from other runs. |

Unlike the direct worker command used by the quickstart, the factory uses the
project name to discover the manager and maintains the requested worker
population. Catalog discovery requires internet access.

By default, `vine_factory` uses one shared factory scratch directory per user.
A worker that remains briefly after `Ctrl-C` can keep files in that directory
busy. This example instead uses `$HOME/vine_scratch/<MANAGER_NAME>`. The
manager name includes the username and process ID, so every run receives a new
factory scratch directory and does not overwrite another run's `vine_worker`
executable. The 60-second worker timeout also limits how long a worker can
remain after the manager or factory has stopped.

This tutorial deliberately leaves worker cores, memory, and disk unspecified.
For other applications and HPC batch systems, the factory can select a
different batch type, request worker resources, read a configuration file, and
manage a larger worker range. See the official
[TaskVine factory overview](https://cctools.readthedocs.io/en/stable/taskvine/#managing-workers-with-the-taskvine-factory)
and [`vine_factory` command reference](https://cctools.readthedocs.io/en/stable/man_pages/vine_factory/).

## 5. Inspect the results

Return to the manager terminal. The two tasks may finish in either order.

You should finish with output similar to:

```text
Completed A x B on <WORKER_ADDRESS>: [[19.0, 22.0], [43.0, 50.0]]
Completed C x D on <WORKER_ADDRESS>: [[6.0, 2.0], [8.0, 4.0]]

File-based PythonTask matrix multiplication complete.
Outputs: outputs/result-ab.csv and outputs/result-cd.csv
```

Inspect the returned files:

```bash
cat outputs/result-ab.csv
cat outputs/result-cd.csv
```

After the manager completes, return to the factory terminal and press
`Ctrl-C`. The factory is a long-running worker-management process and does not
exit merely because one manager run has finished.

## 6. Connect the code to the execution model

The full program is `matrix-files.py`. The sections below isolate the important
TaskVine concepts.

### Define the worker function

```python
def multiply_matrix_files(input_a, input_b, output):
    import numpy as np

    matrix_a = np.loadtxt(input_a, delimiter=",")
    matrix_b = np.loadtxt(input_b, delimiter=",")
    result = np.matmul(matrix_a, matrix_b)
    np.savetxt(output, result, delimiter=",", fmt="%g")
    return result.tolist()
```

The worker function contains every step it needs: importing NumPy, loading both
inputs, multiplying them, writing the output, and returning the result. NumPy
is an external dependency, so it must be available in the environment used by
the manager and workers.

### Create a named manager and factory scratch directory

```python
manager_name = f"taskvine-matrix-files-{getpass.getuser()}-{os.getpid()}"
scratch_dir = Path.home() / "vine_scratch" / manager_name
scratch_dir.mkdir(parents=True, exist_ok=True)
manager = vine.Manager(port=0, name=manager_name)
```

Port `0` selects an available port. The project name is advertised through the
TaskVine catalog, allowing `vine_factory --manager-name` to discover the
manager without copying its hostname and port.

The username distinguishes participants, while the process ID gives every run
a fresh name. The same manager name also gives the factory an isolated scratch
directory under the participant's home directory.

### Declare manager-side files

```python
matrix_a = manager.declare_file(str(DATA_DIR / "matrix-a.csv"))
matrix_b = manager.declare_file(str(DATA_DIR / "matrix-b.csv"))
result_ab = manager.declare_file(str(OUTPUT_DIR / "result-ab.csv"))
```

Files are declared before tasks consume or produce them. The input declarations
identify existing manager-side files. The output declaration identifies where
TaskVine should materialize a returned file.

### Attach files using sandbox names

```python
task_ab = vine.PythonTask(
    multiply_matrix_files,
    "matrix-a.csv",
    "matrix-b.csv",
    "result.csv",
)
task_ab.add_input(matrix_a, "matrix-a.csv")
task_ab.add_input(matrix_b, "matrix-b.csv")
task_ab.add_output(result_ab, "result.csv")
task_ab.set_tag("A x B")
task_ab.set_cores(1)
manager.submit(task_ab)
```

Every task executes in a private worker sandbox. The remote names passed to
`add_input` and `add_output` must match the filenames used by the Python
function.

TaskVine transfers the two inputs into the sandbox, executes
`multiply_matrix_files`, retrieves `result.csv`, and materializes it as
`outputs/result-ab.csv` on the manager side. The returned matrix remains
available separately as the PythonTask's `completed.output` value.

### Collect returned Python values

```python
while not manager.empty():
    completed = manager.wait(5)
    if not completed:
        continue

    result = completed.output
```

`wait(5)` returns a completed task or returns nothing after five seconds. The
application continues waiting while submitted tasks remain. Results may arrive
in either order.

Unlike the quickstart's command task, `completed.output` is not captured
command-line text. For a PythonTask, it is the value returned by
`multiply_matrix_files`.

## Task versus PythonTask

| `vine.Task` | `vine.PythonTask` |
| --- | --- |
| Executes a Unix command line | Executes a Python function |
| Quickstart runs `grep` and `wc` | Matrix example runs `multiply_matrix_files` |
| Standard output is command text | Output is the function's Python return value |
| Useful for commands, scripts, and executables | Useful for Python-native computation |
| Input and output files may be attached | Inherits Task file and resource methods |

Both task types are submitted with `manager.submit`, scheduled on workers, and
returned through `manager.wait`.

## Further reading

- [TaskVine documentation](https://cctools.readthedocs.io/en/stable/taskvine/)
- [Python Tasks](https://cctools.readthedocs.io/en/stable/taskvine/#python-tasks)
- [TaskVine Factory manual](https://cctools.readthedocs.io/en/stable/man_pages/vine_factory/)

## TaskVine hands-on navigation

- Return to the [TaskVine hands-on exercises](hands-on.md).
- Review the [TaskVine Quickstart](quickstart.md).
- Continue to [MobileNet Batch Inference](mobilenet.md).
