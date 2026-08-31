#!/usr/bin/env python3
"""Submit one command-only matrix multiplication task to TaskVine."""

import getpass
import json
import shlex
import textwrap

import ndcctools.taskvine as vine


MATRIX_A = [[1, 2], [3, 4]]
MATRIX_B = [[5, 6], [7, 8]]
EXPECTED_RESULT = [[19, 22], [43, 50]]


# The manager coordinates tasks. Port 0 asks the operating system to choose an
# available local port, which is useful when several tutorial users share a host.
manager_name = f"matrix-basic-{getpass.getuser()}"
manager = vine.Manager(port=0, name=manager_name)

print(f"Manager name: {manager_name}")
print(f"Listening on port: {manager.port}")
print("\nIn a second terminal, activate the same environment and run:")
print(
    "vine_worker --single-shot --cores=1 --memory=2048 --disk=2048 "
    f"localhost {manager.port}"
)


# This first example declares no files. The two small matrices and the worker
# program are encoded directly in the command, and the result returns on stdout.
worker_program = textwrap.dedent(
    f"""
    import json

    matrix_a = {MATRIX_A!r}
    matrix_b = {MATRIX_B!r}

    result = [
        [sum(a * b for a, b in zip(row, column)) for column in zip(*matrix_b)]
        for row in matrix_a
    ]
    print(json.dumps(result))
    """
)
command = f"python3 -c {shlex.quote(worker_program)}"

task = vine.Task(command)
task.set_cores(1)
task_id = manager.submit(task)

print(f"\nSubmitted task {task_id}: {MATRIX_A} x {MATRIX_B}")
print("Waiting for the worker...")

while not manager.empty():
    completed = manager.wait(5)
    if not completed:
        continue
    if not completed.successful():
        raise RuntimeError(
            f"Task {completed.id} failed with TaskVine result "
            f"{completed.result}: {completed.output.strip()}"
        )

    result = json.loads(completed.output)
    if result != EXPECTED_RESULT:
        raise RuntimeError(
            f"Task {completed.id} returned {result}; expected {EXPECTED_RESULT}"
        )
    print(f"Task {completed.id} completed on {completed.addrport}")
    print(f"Result: {result}")

print("\nBasic matrix multiplication complete.")
