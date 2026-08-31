#!/usr/bin/env python3
"""Multiply two pairs of declared CSV matrices with TaskVine PythonTask."""

import getpass
import os
from pathlib import Path

import ndcctools.taskvine as vine


EXAMPLE_DIR = Path(__file__).resolve().parent
DATA_DIR = EXAMPLE_DIR / "data"
OUTPUT_DIR = EXAMPLE_DIR / "outputs"


def multiply_matrix_files(input_a, input_b, output):
    """Read two CSV matrices, multiply them, and write the result as CSV.

    This function is self-contained because PythonTask executes it on a worker.
    """
    import numpy as np

    matrix_a = np.loadtxt(input_a, delimiter=",")
    matrix_b = np.loadtxt(input_b, delimiter=",")
    result = np.matmul(matrix_a, matrix_b)
    np.savetxt(output, result, delimiter=",", fmt="%g")
    return result.tolist()


def main():
    manager_name = f"taskvine-matrix-files-{getpass.getuser()}-{os.getpid()}"
    manager = vine.Manager(port=0, name=manager_name)

    print(f"Manager name: {manager_name}")
    print(f"Listening on port: {manager.port}")
    print("\nIn a second terminal, activate this environment and run:")
    print(
        "vine_factory -T local --min-workers=1 --max-workers=2 "
        f"--manager-name {manager_name}"
    )

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Declare four manager-side inputs and two manager-side outputs.
    matrix_a = manager.declare_file(str(DATA_DIR / "matrix-a.csv"))
    matrix_b = manager.declare_file(str(DATA_DIR / "matrix-b.csv"))
    matrix_c = manager.declare_file(str(DATA_DIR / "matrix-c.csv"))
    matrix_d = manager.declare_file(str(DATA_DIR / "matrix-d.csv"))
    result_ab = manager.declare_file(str(OUTPUT_DIR / "result-ab.csv"))
    result_cd = manager.declare_file(str(OUTPUT_DIR / "result-cd.csv"))

    # The first PythonTask reads A and B from its private worker sandbox.
    task_ab = vine.PythonTask(
        multiply_matrix_files,
        "matrix-a.csv",
        "matrix-b.csv",
        "result.csv",
    )
    task_ab.add_input(matrix_a, "matrix-a.csv")
    task_ab.add_input(matrix_b, "matrix-b.csv")
    task_ab.add_output(result_ab, "result.csv")
    task_ab.set_tag("A x B")
    task_ab.set_cores(1)
    manager.submit(task_ab)

    # The second PythonTask repeats the same operation for C and D.
    task_cd = vine.PythonTask(
        multiply_matrix_files,
        "matrix-c.csv",
        "matrix-d.csv",
        "result.csv",
    )
    task_cd.add_input(matrix_c, "matrix-c.csv")
    task_cd.add_input(matrix_d, "matrix-d.csv")
    task_cd.add_output(result_cd, "result.csv")
    task_cd.set_tag("C x D")
    task_cd.set_cores(1)
    manager.submit(task_cd)

    print("\nSubmitted two file-based PythonTasks. Waiting for the factory worker...")
    while not manager.empty():
        completed = manager.wait(5)
        if not completed:
            continue

        if not completed.successful():
            raise RuntimeError(
                f"Task {completed.tag} failed with TaskVine result "
                f"{completed.result}"
            )
        if isinstance(completed.output, Exception):
            raise RuntimeError(
                f"Task {completed.tag} raised {completed.output!r}"
            )

        print(
            f"Completed {completed.tag} on {completed.addrport}: "
            f"{completed.output}"
        )

    print("\nFile-based PythonTask matrix multiplication complete.")
    print("Outputs: outputs/result-ab.csv and outputs/result-cd.csv")


if __name__ == "__main__":
    main()
