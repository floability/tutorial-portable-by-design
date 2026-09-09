# Matrix Multiplication with TaskVine

The quickstart used `vine.Task` to execute a Linux command. This exercise introduces `vine.PythonTask`, which executes a Python function with Python arguments and returns the function's Python value as `task.output`.

Two complete versions are provided:

| Example | Data source | TaskVine features |
| --- | --- | --- |
| `matrix-basic` | Four matrices hardcoded in Python | Python functions, PythonTask arguments, return values, and manual task submission |
| `matrix-files` | Four matrices stored as CSV files | PythonTask plus declared inputs, sandbox filenames, and declared outputs |

You may run either example. Both use the same environment-creation and `vine_factory` procedure. During the live tutorial, the accompanying slides build the application piece by piece before reviewing the completed code.

## 1. Choose an example

For the basic version:

```bash
cd ~/tutorial/examples/taskvine/matrix-basic
```

For the file-based version:

```bash
cd ~/tutorial/examples/taskvine/matrix-files
```

The remainder of the run procedure is the same for either directory.

## 2. Create the matrix environment

Create a new Conda environment from the selected example's `environment.yml`:

```bash
conda env create --file environment.yml
conda activate taskvine-matrix
```

Both examples provide the same environment specification:

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
| NumPy | Implements matrix multiplication and reads or writes CSV matrices. |

A PythonTask serializes Python code and values; it does not automatically install imported third-party libraries. Because `multiply_matrix` imports NumPy, NumPy must be available in the worker's Python environment. In this local exercise, starting both the manager and `vine_factory` after activating `taskvine-matrix` gives them the same environment.

If you already created `taskvine-matrix` while running the other version, do not create it again. Activate the existing environment:

```bash
conda activate taskvine-matrix
```

Confirm the important imports:

```bash
python -c "import cloudpickle, numpy; import ndcctools.taskvine; print('PythonTask environment: OK')"
```

## 3. Start the manager application

In the first terminal, run the program in your selected directory.

Basic version:

```bash
python matrix-basic.py
```

File-based version:

```bash
python matrix-files.py
```

Each program creates a manager with a unique project name, submits two tasks, prints the manager's selected port, and waits:

```text
Manager name: MANAGER_NAME
Listening on port: PORT

In a second terminal, activate this environment and run:
vine_factory ... --manager-name MANAGER_NAME

Submitted two PythonTasks. Waiting for the factory worker...
```

Leave the manager running.

## 4. Start a local TaskVine factory

Open a second terminal on the same tutorial server or self-managed Linux system. Activate the matrix environment:

```bash
conda activate taskvine-matrix
```

Copy the complete `vine_factory` command printed by the manager and run it in the second terminal. It will look like:

```bash
vine_factory -T local --min-workers=1 --max-workers=2 \
  --manager-name MANAGER_NAME
```

Use the actual manager name printed by your program.

The options have distinct purposes:

| Option | Meaning |
| --- | --- |
| `-T local` | Launch workers as local processes instead of submitting them to an HPC batch system. |
| `--manager-name` | Find the named manager through the TaskVine catalog. |
| `--min-workers=1` | Maintain at least one worker while the manager is active. |
| `--max-workers=2` | Allow the factory to scale up to two workers when tasks are waiting. |

Unlike the direct worker command used by the quickstart, the factory uses the project name to discover the manager and maintains the requested worker population. Catalog discovery requires internet access.

This tutorial deliberately leaves worker cores, memory, and disk unspecified. For other applications and HPC batch systems, the factory can select a different batch type, request worker resources, read a configuration file, and manage a larger worker range. See the official [TaskVine factory overview](https://cctools.readthedocs.io/en/stable/taskvine/#managing-workers-with-the-taskvine-factory) and [`vine_factory` command reference](https://cctools.readthedocs.io/en/stable/man_pages/vine_factory/).

## 5. Inspect the results

Return to the manager terminal.

The basic example should finish with:

```text
Completed A x B on WORKER_ADDRESS: [[19, 22], [43, 50]]
Completed C x D on WORKER_ADDRESS: [[6, 2], [8, 4]]

Basic PythonTask matrix multiplication complete.
```

The file-based example returns the same Python values and two declared files:

```text
Completed A x B on WORKER_ADDRESS: [[19.0, 22.0], [43.0, 50.0]]
Completed C x D on WORKER_ADDRESS: [[6.0, 2.0], [8.0, 4.0]]

File-based PythonTask matrix multiplication complete.
Outputs: outputs/result-ab.csv and outputs/result-cd.csv
```

For the file-based version, inspect those outputs:

```bash
cat outputs/result-ab.csv
cat outputs/result-cd.csv
```

After the manager completes, return to the factory terminal and press `Ctrl-C`. The factory is a long-running worker-management process and does not exit merely because one manager run has finished.

## 6. Build the basic application piece by piece

The full program is `matrix-basic.py`. The sections below isolate the important TaskVine concepts.

### Define an ordinary Python function

```python
def multiply_matrix(matrix_a, matrix_b):
    import numpy as np

    return np.matmul(matrix_a, matrix_b).tolist()
```

`multiply_matrix` is an ordinary Python function. It knows nothing about TaskVine: it receives two matrices, uses NumPy to multiply them, and returns the product as nested Python lists.

The import is inside the function because this function executes on a worker. Serialization transfers the function definition, but the actual `numpy` package comes from the worker environment created from `environment.yml`.

### Create a named manager

```python
manager_name = f"taskvine-matrix-basic-{getpass.getuser()}-{os.getpid()}"
manager = vine.Manager(port=0, name=manager_name)
```

Port `0` selects an available port. The project name is advertised through the TaskVine catalog, allowing `vine_factory --manager-name` to discover the manager without copying its hostname and port.

The username distinguishes participants, while the process ID gives every run a fresh name. This prevents a new factory from matching a briefly retained catalog record from an earlier run.

### Define four matrices

```python
matrix_a = [[1, 2], [3, 4]]
matrix_b = [[5, 6], [7, 8]]
matrix_c = [[2, 0], [0, 2]]
matrix_d = [[3, 1], [4, 2]]
```

These four values form two independent computations: `A × B` and `C × D`.

### Create two PythonTasks manually

```python
task_ab = vine.PythonTask(multiply_matrix, matrix_a, matrix_b)
task_ab.set_tag("A x B")
task_ab.set_cores(1)
task_ab_id = manager.submit(task_ab)

task_cd = vine.PythonTask(multiply_matrix, matrix_c, matrix_d)
task_cd.set_tag("C x D")
task_cd.set_cores(1)
task_cd_id = manager.submit(task_cd)
```

A PythonTask receives a function followed by its arguments. TaskVine serializes the function and arguments, sends them to a compatible worker, invokes the function, and returns its Python value in `completed.output`.

The tasks are written separately rather than generated by a loop so that the complete definition and submission of each task is visible.

`set_cores(1)` tells TaskVine that each task needs one core. TaskVine matches task requirements against the capacity advertised by workers.

### Collect returned Python values

```python
while not manager.empty():
    completed = manager.wait(5)
    if not completed:
        continue

    result = completed.output
```

`wait(5)` returns a completed task or returns nothing after five seconds. The application continues waiting while submitted tasks remain. Results may arrive in either order.

Unlike the quickstart's command task, `completed.output` is not captured command-line text. For a PythonTask, it is the value returned by `multiply_matrix`.

## 7. Extend the application with files

The file-based task performs the same multiplication, but its worker function now contains every step it needs: importing NumPy, loading both inputs, multiplying them, writing the output, and returning the result. It does not call another function defined elsewhere in the manager program.

```python
def multiply_matrix_files(input_a, input_b, output):
    import numpy as np

    matrix_a = np.loadtxt(input_a, delimiter=",")
    matrix_b = np.loadtxt(input_b, delimiter=",")
    result = np.matmul(matrix_a, matrix_b)
    np.savetxt(output, result, delimiter=",", fmt="%g")
    return result.tolist()
```

Keeping the worker function self-contained makes its execution requirements visible and avoids relying on TaskVine's serializer to capture another project-level function implicitly. NumPy is still an external software dependency, so it must be installed in the environment used by both the manager and workers.

### Declare manager-side files

```python
matrix_a = manager.declare_file(str(DATA_DIR / "matrix-a.csv"))
matrix_b = manager.declare_file(str(DATA_DIR / "matrix-b.csv"))
result_ab = manager.declare_file(str(OUTPUT_DIR / "result-ab.csv"))
```

According to TaskVine's data model, files are declared before tasks consume or produce them. The input declarations identify existing manager-side files. The output declaration identifies where TaskVine should materialize a returned file.

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
```

Every task executes in a private worker sandbox. The remote names passed to `add_input` and `add_output` must match the filenames used by the Python function.

TaskVine transfers the two inputs into the sandbox, executes `multiply_matrix_files`, retrieves `result.csv`, and materializes it as `outputs/result-ab.csv` on the manager side. The returned matrix remains available separately as the PythonTask's `completed.output` value.

## Task versus PythonTask

| `vine.Task` | `vine.PythonTask` |
| --- | --- |
| Executes a Unix command line | Executes a Python function |
| Quickstart runs `grep` and `wc` | Matrix examples run `multiply_matrix` |
| Standard output is command text | Output is the function's Python return value |
| Useful for commands, scripts, and executables | Useful for Python-native computation |
| Input and output files may be attached | Inherits Task file and resource methods |

Both task types are submitted with `manager.submit`, scheduled on workers, and returned through `manager.wait`.

## Further reading

- [TaskVine documentation](https://cctools.readthedocs.io/en/stable/taskvine/)
- [Python Tasks](https://cctools.readthedocs.io/en/stable/taskvine/#python-tasks)
- [TaskVine Factory manual](https://cctools.readthedocs.io/en/stable/man_pages/vine_factory/)

## TaskVine hands-on navigation

- Return to the [TaskVine hands-on exercises](hands-on.md).
- Review the [TaskVine Quickstart](quickstart.md).
- Continue to [MobileNet Batch Inference](mobilenet.md).
