# File-Based Matrix Multiplication with PythonTask

This example keeps the same NumPy-based `multiply_matrix` function as the basic version, but its two PythonTasks use NumPy to read declared CSV inputs from worker sandboxes and write declared CSV outputs for TaskVine to return.

Follow the complete participant instructions in [Matrix Multiplication with TaskVine](../../../docs/02-taskvine/matrix.md).

The four input matrices form two manually submitted tasks:

```text
matrix-a.csv × matrix-b.csv → outputs/result-ab.csv
matrix-c.csv × matrix-d.csv → outputs/result-cd.csv
```
