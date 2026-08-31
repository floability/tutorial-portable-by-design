#!/usr/bin/env python3
"""Multiply several independent pairs of CSV matrices with TaskVine."""

import getpass
from pathlib import Path

import ndcctools.taskvine as vine


EXAMPLE_DIR = Path(__file__).resolve().parent
DATA_DIR = EXAMPLE_DIR / "data"
OUTPUT_DIR = EXAMPLE_DIR / "outputs"

MATRIX_PAIRS = [
    ("square-2x2", "pair-01-a.csv", "pair-01-b.csv"),
    ("rectangular", "pair-02-a.csv", "pair-02-b.csv"),
    ("identity", "pair-03-a.csv", "pair-03-b.csv"),
]


# Step 1: Create the manager and tell the participant how to start one worker.
manager_name = f"matrix-files-{getpass.getuser()}"
manager = vine.Manager(port=0, name=manager_name)

print(f"Manager name: {manager_name}")
print(f"Listening on port: {manager.port}")
print("\nIn a second terminal, activate the same environment and run:")
print(
    "vine_worker --single-shot --cores=1 --memory=2048 --disk=2048 "
    f"localhost {manager.port}"
)


# Step 2: Declare the program once. TaskVine can cache this common input and
# reuse it for every multiplication task sent to a worker.
multiply_program = manager.declare_file(
    str(EXAMPLE_DIR / "multiply_csv.py"),
    cache=True,
)

OUTPUT_DIR.mkdir(exist_ok=True)
submitted = {}


# Step 3: Turn each independent matrix pair into one task. Local filenames are
# mapped to simple sandbox names that are identical for every task.
for label, matrix_a_name, matrix_b_name in MATRIX_PAIRS:
    matrix_a = manager.declare_file(str(DATA_DIR / matrix_a_name), cache=True)
    matrix_b = manager.declare_file(str(DATA_DIR / matrix_b_name), cache=True)
    output_path = OUTPUT_DIR / f"{label}.csv"
    result_file = manager.declare_file(str(output_path))

    task = vine.Task(
        "python3 multiply_csv.py matrix-a.csv matrix-b.csv result.csv"
    )
    task.add_input(multiply_program, "multiply_csv.py")
    task.add_input(matrix_a, "matrix-a.csv")
    task.add_input(matrix_b, "matrix-b.csv")
    task.add_output(result_file, "result.csv")
    task.set_tag(label)
    task.set_cores(1)
    task.set_memory(256)
    task.set_disk(256)

    task_id = manager.submit(task)
    submitted[task_id] = (label, output_path)

print(f"\nSubmitted {len(submitted)} independent matrix tasks.")
print("Waiting for the worker...")


# Step 4: Collect tasks in completion order. Task IDs connect returned tasks to
# the local output paths chosen when they were submitted.
succeeded = 0
while not manager.empty():
    completed = manager.wait(5)
    if not completed:
        continue

    label, output_path = submitted[completed.id]
    if not completed.successful():
        print(
            f"FAILED {label}: TaskVine result={completed.result} "
            f"output={completed.output.strip()!r}"
        )
        continue

    succeeded += 1
    print(
        f"Completed {label!r} on {completed.addrport}: "
        f"{output_path.relative_to(EXAMPLE_DIR)}"
    )

if succeeded != len(submitted):
    raise SystemExit(
        f"Only {succeeded} of {len(submitted)} matrix tasks succeeded."
    )

print(f"\nData-parallel matrix multiplication complete: {succeeded} tasks.")
