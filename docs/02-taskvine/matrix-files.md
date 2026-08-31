# Data-Parallel Matrix Multiplication

The quickstart submitted one command with fixed matrices and returned a small result through standard output. This exercise keeps the same computation but introduces TaskVine's data-management features.

You will submit three independent matrix multiplications. Each task receives two CSV inputs and a shared Python program in its private worker sandbox. TaskVine returns each result as a declared output file.

## What changes from the quickstart?

| Basic example | This example |
| --- | --- |
| One task | Three independent tasks |
| Matrices embedded in the command | Matrices stored in CSV files |
| No declared files | Program, inputs, and outputs declared to TaskVine |
| Result captured from standard output | Result transferred back as a CSV file |
| One completion | Results collected in whichever order they finish |

## 1. Inspect the application

Enter the example directory:

```bash
cd ~/tutorial/examples/taskvine/matrix-files
find . -maxdepth 2 -type f | sort
```

You should see:

```text
./README.md
./data/pair-01-a.csv
./data/pair-01-b.csv
./data/pair-02-a.csv
./data/pair-02-b.csv
./data/pair-03-a.csv
./data/pair-03-b.csv
./environment.yml
./matrix-files.py
./multiply_csv.py
```

The files have separate roles:

- `matrix-files.py` is the TaskVine manager application.
- `multiply_csv.py` runs inside each task sandbox.
- `data/` contains three independent pairs of input matrices.
- `outputs/` will be created when TaskVine returns the results.

Inspect one pair:

```bash
cat data/pair-01-a.csv
cat data/pair-01-b.csv
```

These matrices multiply as follows:

```text
1  2       5  6       19  22
3  4   ×   7  8   =   43  50
```

## 2. Start the manager

In your first terminal, run:

```bash
python matrix-files.py
```

The application creates its manager, declares the files, and submits all three tasks before a worker is available:

```text
Manager name: matrix-files-USERNAME
Listening on port: PORT

In a second terminal, activate the same environment and run:
vine_worker ... localhost PORT

Submitted 3 independent matrix tasks.
Waiting for the worker...
```

Leave this terminal running.

## 3. Start a local worker

Open or return to your second terminal. If necessary, connect to the live server and activate its shared environment:

```bash
ssh USERNAME@SERVER
source /opt/tutorial/activate.sh
```

Self-managed participants should instead activate their Conda environment:

```bash
conda activate portable-by-design
```

Copy and run the complete worker command printed by `matrix-files.py`. It will resemble:

```bash
vine_worker --single-shot --cores=1 --memory=2048 --disk=2048 localhost PORT
```

The one-core worker executes the three ready tasks one at a time. A larger worker or several workers could execute independent tasks concurrently without changing the manager program.

## 4. Observe dynamic completion

Return to the manager terminal. A successful run reports every returned output:

```text
Completed 'square-2x2' on WORKER_ADDRESS: outputs/square-2x2.csv
Completed 'rectangular' on WORKER_ADDRESS: outputs/rectangular.csv
Completed 'identity' on WORKER_ADDRESS: outputs/identity.csv

Data-parallel matrix multiplication complete: 3 tasks.
```

The order is not guaranteed. TaskVine returns whichever completed task is available when the manager calls `wait`.

Inspect the transferred results:

```bash
for result in outputs/*.csv; do
  echo "--- $result"
  cat "$result"
done
```

Expected result files include:

```text
--- outputs/rectangular.csv
58,64
139,154

--- outputs/square-2x2.csv
19,22
43,50
```

## 5. Understand the TaskVine features

Open `matrix-files.py` while following the sections below:

```bash
less matrix-files.py
```

### Declare a reusable program

```python
multiply_program = manager.declare_file(
    str(EXAMPLE_DIR / "multiply_csv.py"),
    cache=True,
)
```

`declare_file` tells TaskVine about a manager-side file. Declaring a file does not immediately copy it. TaskVine transfers it when a selected worker needs it.

The `cache=True` setting allows a worker to retain this immutable file and reuse it for later tasks. All three tasks use the same multiplication program, so it needs to be transferred to a worker only once.

### Declare each task's data

```python
matrix_a = manager.declare_file(str(DATA_DIR / matrix_a_name), cache=True)
matrix_b = manager.declare_file(str(DATA_DIR / matrix_b_name), cache=True)
```

These declarations identify the local CSV inputs. Each pair is independent, allowing TaskVine to schedule its multiplication separately.

### Map inputs into the task sandbox

```python
task.add_input(multiply_program, "multiply_csv.py")
task.add_input(matrix_a, "matrix-a.csv")
task.add_input(matrix_b, "matrix-b.csv")
```

Every task runs in a private sandbox. The second argument is the filename visible inside that sandbox. Manager-side files can have unique descriptive names while every task uses the same simple command:

```python
task = vine.Task(
    "python3 multiply_csv.py matrix-a.csv matrix-b.csv result.csv"
)
```

This separation between a file's manager-side location and sandbox name is central to TaskVine's data model.

### Declare an output file

```python
result_file = manager.declare_file(str(output_path))
task.add_output(result_file, "result.csv")
```

The task writes `result.csv` inside its sandbox. TaskVine retrieves that file and materializes it at the corresponding path under `outputs/` on the manager side.

Only declared outputs are transferred back as files. Standard output is still available through `completed.output`, but this application uses it only for a short status message.

### Add identity and resource requirements

```python
task.set_tag(label)
task.set_cores(1)
task.set_memory(256)
task.set_disk(256)
```

The tag associates a meaningful label such as `rectangular` with a task. Resource requests tell TaskVine what the command needs. A task becomes eligible only on a worker with sufficient currently available cores, memory, and disk. TaskVine uses the worker's advertised capacity and the task requests to decide which tasks can run together.

### Submit independent work

```python
task_id = manager.submit(task)
submitted[task_id] = (label, output_path)
```

The loop submits every matrix pair without waiting for the preceding pair. This exposes all ready work to TaskVine, which is what permits parallel execution when more resources are available.

### Collect results as they finish

```python
while not manager.empty():
    completed = manager.wait(5)
```

`manager.empty()` becomes true after no submitted tasks remain. Until then, `wait` returns completed tasks independently of submission order. The application uses each returned task ID to recover its label and expected output path.

## 6. Extend the workflow

Add a fourth independent multiplication to see how the application grows by data rather than by duplicated control logic.

Create two compatible matrices:

```bash
printf '2,0\n0,2\n' > data/pair-04-a.csv
printf '3,1\n4,2\n' > data/pair-04-b.csv
```

In `matrix-files.py`, append this entry to `MATRIX_PAIRS`:

```python
("scaled-2x2", "pair-04-a.csv", "pair-04-b.csv"),
```

Run the manager and a newly printed worker command again. The final summary should now report four successful tasks, and the additional output should be:

```text
6,2
8,4
```

Remove the two added inputs and the `MATRIX_PAIRS` entry if you want to restore the original example.

## What you have learned

- TaskVine transfers declared inputs only when tasks need them.
- Cached files can be reused across tasks on a worker.
- Task sandbox names are independent of manager-side paths.
- Declared outputs are returned to chosen manager-side locations.
- Submitting all independent tasks exposes parallelism to TaskVine.
- Task tags and IDs connect dynamically returned results to application meaning.
- Resource requests guide TaskVine's scheduling decisions.

The next documented example will introduce TaskVine Function Calls and Function Libraries for reusable worker-side state.
