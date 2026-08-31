# Matrix Multiplication with PythonTask

This example defines a plain Python function named `multiply_matrix`. Its `main` function hardcodes four matrices and manually creates two TaskVine `PythonTask` objects, one for each independent matrix pair.

Follow the complete participant instructions in [Matrix Multiplication with TaskVine](../../../docs/02-taskvine/matrix.md).

The example contains no workflow data files. TaskVine serializes the Python function, its arguments, and its return value with `cloudpickle`. NumPy performs the multiplication and must be installed in the environment used by both the manager and factory workers.
