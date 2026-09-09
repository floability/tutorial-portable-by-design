# TaskVine Hands-on Exercises

The exercises progress from a Linux command to Python functions, declared data,
and persistent serverless execution. Complete them in order during the tutorial,
or use each page independently afterward.

## 1. TaskVine Quickstart

[Run the TaskVine Quickstart](quickstart.md) to create a manager, submit five
Linux command tasks, declare a shared remote input, connect a worker directly,
and collect standard output.

This is the environment and access validation exercise.

## 2. Matrix Multiplication

[Run Matrix Multiplication with TaskVine](matrix.md) to execute Python functions
with `PythonTask` and start workers through `vine_factory`. Choose either the
in-memory program or its file-based extension.

This exercise introduces Python return values, resource requirements, declared
inputs and outputs, and worker sandbox filenames.

## 3. MobileNet Batch Inference

[Run MobileNet Batch Inference](mobilenet.md) to compare two versions of the
same image-classification application: ordinary PythonTasks that load the model
inside each task, and Function Calls that reuse a model held by a persistent
Function Library.

This is the advanced exercise. It may be demonstrated during the live session
and completed independently afterward.
