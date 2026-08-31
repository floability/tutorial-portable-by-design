# TaskVine

TaskVine provides the distributed execution layer used throughout this tutorial. A TaskVine application creates a manager, submits tasks and their data dependencies, and collects results. Workers connect to the manager, request ready tasks, and execute them in private sandboxes.

## Execution model

The application owns the workflow logic. Its manager describes and coordinates work, while workers supply the resources that execute it:

```text
TaskVine application
        │
        ▼
     Manager ─── defines tasks and tracks files
        │
        ├──── Worker ─── task sandbox
        ├──── Worker ─── task sandbox
        └──── Worker ─── task sandbox
```

Workers request ready tasks from the manager. They may join or leave while the application is running, and the manager assigns work according to data availability and requested resources.

On an HPC system, the batch scheduler allocates worker processes to nodes. TaskVine then schedules the application's finer-grained tasks across those workers. It complements the site scheduler rather than replacing it.

## Core TaskVine features

| Feature | Role in an application |
| --- | --- |
| Manager | Coordinates tasks, files, workers, and results. |
| Command task | Uses `vine.Task` to describe a Unix command line executed in a worker sandbox. |
| Python task | Uses `vine.PythonTask` to execute a Python function with Python arguments. |
| Submission | Makes a task available for TaskVine to schedule. |
| `wait` | Returns completed tasks to the application in dynamic completion order. |
| File declarations | Describe inputs and outputs before tasks use them. |
| Sandbox mappings | Give manager-side files predictable names inside individual tasks. |
| File caching | Allows workers to reuse immutable inputs across tasks. |
| Resource requests | Match task core, memory, disk, and GPU needs to worker capacity. |
| Function Calls | Invoke Python functions through persistent Function Libraries. |

Function Calls provide TaskVine's serverless-style execution model. A Function Library can initialize expensive reusable state—such as a machine-learning model—once on a worker and serve many lightweight calls. A later advanced example will explore this model.

## Hands-on progression

### 1. TaskVine quickstart

Start with the [**TaskVine Quickstart**](quickstart.md). You will use standard `vine.Task` objects to run Linux `grep` and `wc` commands, observe the manager waiting for resources, and connect one worker directly.

### 2. Matrix multiplication with PythonTask

Continue with [**Matrix Multiplication with TaskVine**](matrix.md). You may run a hardcoded or file-based version. Both use PythonTask to execute a Python function, and both obtain a local worker through `vine_factory`. The file-based version adds explicit input and output declarations.

Together, the exercises distinguish Unix command tasks from Python function tasks before introducing Function Calls and reusable worker-side libraries.
