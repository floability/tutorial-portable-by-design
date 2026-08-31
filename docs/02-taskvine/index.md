# TaskVine

TaskVine provides the distributed execution layer used throughout this tutorial. A TaskVine application creates a manager, submits tasks and their data dependencies, and collects results. Workers connect to the manager, request ready tasks, and execute them in private sandboxes.

The live tutorial begins with a short overview of four ideas:

- The application owns the workflow logic.
- The manager coordinates tasks, files, and results.
- Workers provide execution resources and may join or leave while the workflow runs.
- TaskVine complements an HPC batch scheduler by scheduling application tasks on allocated resources.

Start with [**TaskVine Quickstart**](quickstart.md). You will run a prepared manager program, observe it waiting for execution resources, connect one local worker, and complete your first distributed workflow.

The next exercise will examine the Python application and introduce task submission, file declarations, resource requests, and result collection.
