# TaskVine Quickstart

In this exercise, you will start a TaskVine manager, observe it waiting for execution resources, and connect one local worker from a second terminal.

The prepared program submits five word-count tasks. Each task searches for a different word in the same copy of *War and Peace*.

## Before you begin

Complete [Access and Setup](../01-access-and-setup/index.md) before starting this exercise. Both setup routes place the repository at `~/tutorial`.

Enter the first example and check its contents:

```bash
cd ~/tutorial/examples/taskvine/quickstart
ls
```

You should see:

```text
README.md  taskvine-quickstart.py
```

The live server already contains these files. Self-managed participants received them by cloning the repository during setup.

## 1. Start the manager

In your current terminal, run:

```bash
python taskvine-quickstart.py
```

The program will print a manager name containing your username, select an available port, submit five tasks, and then wait:

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

Open another terminal on your computer, connect to the same tutorial server with the credentials on your card, and activate the shared tools:

```bash
ssh USERNAME@SERVER
source /opt/tutorial/activate.sh
```

### Self-managed participants

Open another terminal on the same Linux computer and activate the tutorial environment:

```bash
conda activate portable-by-design
```

## 3. Start the worker

Return briefly to the manager terminal and copy the complete `vine_worker` command it printed. Run that command in the second terminal.

It will look similar to:

```bash
vine_worker localhost PORT
```

Use the actual port printed by your manager instead of `PORT`.

The worker connects locally to your manager and begins requesting tasks. Live participants should run this command on the tutorial server, not on their own laptop.

## 4. Confirm success

Return to the manager terminal. The five tasks may finish in a different order from the order in which they were submitted.

You should finish with:

```text
Quickstart complete: 5 of 5 tasks succeeded.
```

You have now run a TaskVine manager and worker. The manager described the work, the worker provided an execution resource, and TaskVine transferred the shared input and returned each result.

## Reset

The manager exits after all five tasks finish. Return to the worker terminal and press `Ctrl-C` to stop the worker.

If the exercise is interrupted, press `Ctrl-C` once in each terminal. Then restart the manager and use the newly printed worker command because the port may change.

## Progress

```text
[x] Tutorial environment works
[x] TaskVine manager starts
[x] Worker connects
[x] First distributed workflow completes
```

Continue to **TaskVine Application Structure and Execution** *(coming soon)*.
