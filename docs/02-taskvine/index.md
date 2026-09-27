# TaskVine

TaskVine distributes tasks across workers. A TaskVine application starts a
manager, submits tasks and their input files, and collects completed results.
Workers connect to the manager and run those tasks in isolated sandboxes.

## How TaskVine works

```text
Application → Manager → Workers → Results
```

1. The application starts a manager.
2. The application defines files and submits tasks.
3. Workers connect and request ready tasks.
4. Each worker stages the required files and runs the task.
5. The manager returns completed results to the application.

Workers may join or leave while the application is running. On an HPC system,
the batch scheduler provides the worker processes, while TaskVine schedules the
application's tasks across them.

For a complete introduction and API reference, see the
[official TaskVine documentation](https://cctools.readthedocs.io/en/stable/taskvine/).

## Hands-on exercises

Complete the exercises in order:

1. [**TaskVine Quickstart**](quickstart.md) — start a manager and worker, run
   five command tasks, and collect their output.
2. [**Matrix Multiplication**](matrix.md) — run Python functions with
   `PythonTask` and declared input files.
3. [**MobileNet Batch Inference**](mobilenet.md) — compare ordinary
   PythonTasks with a persistent Function Library.

The Quickstart also confirms that your tutorial account and TaskVine
installation are ready.

[**Start with the TaskVine Quickstart →**](quickstart.md)
