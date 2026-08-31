#!/usr/bin/env python3

import getpass

import ndcctools.taskvine as vine


username = getpass.getuser()
manager_name = f"taskvine-quickstart-{username}"

manager = vine.Manager(port=0, name=manager_name)

print(f"Manager name: {manager_name}")
print(f"Listening on port: {manager.port}")
print("\nIn a second terminal, run:")
print(f"vine_worker localhost {manager.port}")

shared_text = manager.declare_url(
    "https://www.gutenberg.org/cache/epub/2600/pg2600.txt",
    cache="workflow",
)

keywords = ["needle", "house", "water", "war", "peace"]

print("\nSubmitting tasks...")
for keyword in keywords:
    task = vine.Task(f"grep -i {keyword} warandpeace.txt | wc")
    task.add_input(shared_text, "warandpeace.txt")
    task.set_cores(1)
    manager.submit(task)

print("Waiting for a worker to connect and complete the tasks...")
succeeded = 0

while not manager.empty():
    completed = manager.wait(5)
    if not completed:
        continue

    if completed.successful():
        succeeded += 1
        print(f"Task {completed.id} succeeded: {completed.output.strip()}")
    else:
        print(f"Task {completed.id} failed: {completed.result}")

print(f"\nQuickstart complete: {succeeded} of {len(keywords)} tasks succeeded.")

if succeeded != len(keywords):
    raise SystemExit(1)
