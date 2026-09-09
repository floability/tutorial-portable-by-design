# TaskVine Quickstart

In this exercise, you will start a TaskVine manager, observe it waiting for execution resources, and connect one local worker from a second terminal.

The prepared program submits five word-count tasks. Each task runs the Linux tools `grep` and `wc` to search for a different word in the same copy of *War and Peace*.

This quickstart uses `vine.Task`, TaskVine's standard command-task interface. A standard task describes a Unix command line. The later matrix exercises use `vine.PythonTask` to execute Python functions instead.

## Before you begin

Complete [Access and Setup](../01-access-and-setup/index.md) before starting. Both setup routes place the repository at `~/tutorial`.

Enter the quickstart directory:

```bash
cd ~/tutorial/examples/taskvine/quickstart
ls
```

You should see:

```text
README.md  taskvine-quickstart.py
```

## 1. Start the manager

In your current terminal, run:

```bash
python taskvine-quickstart.py
```

The program prints a manager name containing your username, selects an available port, submits five tasks, and waits:

```text
Manager name: taskvine-quickstart-USERNAME
Listening on port: PORT

In a second terminal, run:
vine_worker ... localhost PORT

Submitting tasks...
Waiting for a worker to connect and complete the tasks...
```

Nothing is wrong when the program waits here. The manager has work to perform but does not yet have a worker.

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

## 3. Start the worker directly

Return briefly to the manager terminal and copy the complete `vine_worker` command it printed. Run that command in the second terminal.

It will look similar to:

```bash
vine_worker localhost PORT
```

Use the actual port printed by your manager instead of `PORT`. Live participants should run this command on the tutorial server, not on their laptop.

The worker connects directly to the manager and begins requesting tasks. This is the only primary tutorial example that starts a worker directly; later exercises use `vine_factory` to discover a named manager and maintain workers for it.

## 4. Confirm success

Return to the manager terminal. The five tasks may finish in a different order from the order in which they were submitted.

You should finish with:

```text
Quickstart complete: 5 of 5 tasks succeeded.
```

The manager declared one remote file, attached it to five tasks, and captured the standard output from each Linux command.

## 5. Connect the code to the execution model

The essential task definition is:

```python
task = vine.Task(f"grep -i {keyword} warandpeace.txt | wc")
task.add_input(shared_text, "warandpeace.txt")
task.set_cores(1)
manager.submit(task)
```

`vine.Task` receives a command line. When a worker runs this task, TaskVine creates a private sandbox, makes the declared input available as `warandpeace.txt`, and executes the `grep` and `wc` pipeline there.

The command writes its result to standard output, so the manager retrieves it through:

```python
completed.output
```

This model is useful for existing Linux commands, shell scripts, compiled programs, and other command-line applications.

## Reset

The manager exits after all five tasks finish. Return to the worker terminal and press `Ctrl-C` to stop the worker.

If the exercise is interrupted, press `Ctrl-C` once in each terminal. Restart the manager and use the newly printed worker command because its port may change.

## What you have learned

- A TaskVine manager defines and coordinates work.
- A worker supplies execution resources.
- `vine.Task` describes a Unix command line.
- Declared files are mapped into private task sandboxes.
- Task results may complete in a different order from submission.

## TaskVine hands-on navigation

- Return to the [TaskVine hands-on exercises](hands-on.md).
- Continue to [Matrix Multiplication with TaskVine](matrix.md).
- Preview [MobileNet Batch Inference](mobilenet.md).
