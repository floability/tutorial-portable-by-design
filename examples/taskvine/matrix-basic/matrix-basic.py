#!/usr/bin/env python3
"""Multiply two hardcoded matrix pairs with TaskVine PythonTask."""

import getpass
import os

import ndcctools.taskvine as vine


def multiply_matrix(matrix_a, matrix_b):
    """Return the matrix product of matrix_a and matrix_b."""
    import numpy as np

    return np.matmul(matrix_a, matrix_b).tolist()


def main():
    manager_name = f"taskvine-matrix-basic-{getpass.getuser()}-{os.getpid()}"
    manager = vine.Manager(port=0, name=manager_name)

    print(f"Manager name: {manager_name}")
    print(f"Listening on port: {manager.port}")
    print("\nIn a second terminal, activate this environment and run:")
    print(
        "vine_factory -T local --min-workers=1 --max-workers=2 "
        f"--manager-name {manager_name}"
    )

    # Four hardcoded matrices make two independent multiplication tasks.
    matrix_a = [[1, 2], [3, 4]]
    matrix_b = [[5, 6], [7, 8]]
    matrix_c = [[2, 0], [0, 2]]
    matrix_d = [[3, 1], [4, 2]]

    # A PythonTask runs a Python function with Python arguments on a worker.
    task_ab = vine.PythonTask(multiply_matrix, matrix_a, matrix_b)
    task_ab.set_tag("A x B")
    task_ab.set_cores(1)
    manager.submit(task_ab)

    task_cd = vine.PythonTask(multiply_matrix, matrix_c, matrix_d)
    task_cd.set_tag("C x D")
    task_cd.set_cores(1)
    manager.submit(task_cd)

    print("\nSubmitted two PythonTasks. Waiting for the factory worker...")
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

    print("\nBasic PythonTask matrix multiplication complete.")


if __name__ == "__main__":
    main()
