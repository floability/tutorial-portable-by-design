# TaskVine Quickstart: Basic Matrix Multiplication

In this exercise, you will run one matrix-multiplication task with TaskVine. A manager submits the task and waits while a local worker connects from a second terminal, executes the command, and returns its standard output.

The matrices are embedded directly in the command, so this first exercise has no data files to transfer. Its purpose is to validate your environment and introduce the manager–worker execution model with as few moving parts as possible.

## What you will do

1. Start a TaskVine manager.
2. Submit one command task.
3. Start one resource-limited local worker.
4. Receive and validate the result.

## Before you begin

Complete [Access and Setup](../01-access-and-setup/index.md) before starting. Both setup routes place the tutorial repository at `~/tutorial`.

Enter the example directory:

```bash
cd ~/tutorial/examples/taskvine/matrix-basic
ls
```

You should see:

```text
README.md  environment.yml  matrix-basic.py
```

Live participants should already have the shared tutorial tools activated. Self-managed participants should activate their tutorial environment if necessary:

```bash
conda activate portable-by-design
```

## 1. Start the manager

In your first terminal, run:

```bash
python matrix-basic.py
```

The program creates a manager on an available local port and submits one task:

```text
Manager name: matrix-basic-USERNAME
Listening on port: PORT

In a second terminal, activate the same environment and run:
vine_worker ... localhost PORT

Submitted task 1: [[1, 2], [3, 4]] x [[5, 6], [7, 8]]
Waiting for the worker...
```

The program is supposed to wait at this point. The manager has described the work, but no execution resource has connected yet.

Leave this terminal running.

## 2. Open a second terminal

### Live tutorial participants

Open another terminal on your computer, connect to the same tutorial server, and activate the shared tools:

```bash
ssh USERNAME@SERVER
source /opt/tutorial/activate.sh
```

Use the username and server printed on your credential card.

### Self-managed participants

Open another terminal on the same Linux system and activate the tutorial environment:

```bash
conda activate portable-by-design
```

## 3. Start the worker

Return briefly to the manager terminal and copy the complete `vine_worker` command it printed. Run that command in your second terminal.

It will look similar to:

```bash
vine_worker --single-shot --cores=1 --memory=2048 --disk=2048 localhost PORT
```

Use the actual port printed by your manager instead of `PORT`. Live participants must run the worker on the tutorial server, not on their laptop.

The worker options deliberately limit the resources advertised to TaskVine:

| Option | Meaning |
| --- | --- |
| `--single-shot` | Exit after this manager disconnects. |
| `--cores=1` | Advertise one CPU core. |
| `--memory=2048` | Advertise 2,048 MiB of memory. |
| `--disk=2048` | Advertise 2,048 MiB of task workspace. |
| `localhost PORT` | Connect directly to the manager running on the same server. |

## 4. Confirm the result

Return to the manager terminal. It should report the worker address and the validated product:

```text
Task 1 completed on WORKER_ADDRESS
Result: [[19, 22], [43, 50]]

Basic matrix multiplication complete.
```

The manager then exits. Because the worker was started with `--single-shot`, the worker also disconnects and exits automatically.

## 5. Connect the code to the execution model

Open `matrix-basic.py` in an editor or inspect it from the terminal:

```bash
less matrix-basic.py
```

### Create the manager

```python
manager = vine.Manager(port=0, name=manager_name)
```

The manager coordinates tasks and workers. Port `0` asks the operating system to select an available port, avoiding fixed-port conflicts when many participants share the tutorial server.

### Define a command task

```python
task = vine.Task(command)
task.set_cores(1)
```

A `Task` describes a command to execute. This task requests one core. TaskVine will assign it only to a worker that advertises enough available resources.

The two matrices and the worker-side Python program are embedded in `command`. There are no declared files in this first example; the result is printed to the task's standard output.

### Submit the task

```python
task_id = manager.submit(task)
```

Submitting places the task under the manager's control. Submission does not execute the task immediately: a suitable worker must first connect and request work.

### Wait for completion

```python
completed = manager.wait(5)
```

`wait` returns a completed task, or no task when the five-second timeout expires. Real applications usually call it repeatedly while submitted work remains.

### Check success and retrieve output

```python
if not completed.successful():
    raise RuntimeError(...)

result = json.loads(completed.output)
```

The manager checks TaskVine's task result before using the captured standard output. The program also compares the matrix product with the expected answer and exits nonzero if they differ.

## If you need to stop early

Press `Ctrl-C` once in each terminal. Restart the manager before trying again, then use the newly printed worker command because its port may be different.

## What you have learned

- A manager defines and coordinates work.
- A worker supplies execution resources.
- Submitting a task and executing it are separate events.
- Task resource requests are matched against worker resources.
- A command task can return a small result through standard output.

Continue to [**Data-Parallel Matrix Multiplication**](matrix-files.md), where the same computation gains declared input files, output files, and multiple independent tasks.
