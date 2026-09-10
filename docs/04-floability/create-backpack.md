# Create and Run Your Own Backpack

**Session time:** 20 minutes

This exercise uses two creation paths. First, you create a working backpack
from a built-in template and make a small change. Then you package the basic
matrix-multiplication program from the earlier TaskVine exercise.

Both workflows are Python scripts, so run them non-interactively with
`floability execute`.

## Before you begin

Activate the tutorial tools and return to the repository root.

### Live tutorial

```bash
source /opt/tutorial/activate.sh
cd ~/tutorial
```

### Self-managed

```bash
conda activate portable-by-design
cd ~/tutorial
```

Create a directory for the backpacks you build:

```bash
mkdir -p ~/tutorial/created-backpacks
```

## Part 1: Start from a template

Use `--from-template` when you want a complete working starting point. The
`taskvine` template demonstrates manager creation, PythonTask submission, and
result collection without using Floability-managed data.

### 1. Generate the backpack

```bash
floability backpack init \
  --name ~/tutorial/created-backpacks/my-taskvine-backpack \
  --from-template taskvine \
  --script
```

`--script` creates a Python entrypoint instead of the template's default
notebook. Inspect the generated structure:

```bash
find ~/tutorial/created-backpacks/my-taskvine-backpack \
  -maxdepth 2 -type f | sort
```

It contains:

```text
my-taskvine-backpack/
├── compute/
│   └── compute.yml
├── software/
│   └── environment.yml
└── workflow/
    └── my-taskvine-backpack.py
```

### 2. Make a simple workflow change

Open the generated workflow:

```bash
nano ~/tutorial/created-backpacks/my-taskvine-backpack/workflow/my-taskvine-backpack.py
```

Find this line in `worker_function`:

```python
return {"input": value, "output": value * 2}
```

Change only the multiplier so that every worker returns three times its input:

```python
return {"input": value, "output": value * 3}
```

After editing in `nano`, press `Ctrl-O`, then `Enter` to save, and `Ctrl-X` to
exit.

### 3. Pin the software requirements

Open the software specification:

```bash
nano ~/tutorial/created-backpacks/my-taskvine-backpack/software/environment.yml
```

Set its contents to:

```yaml
name: my-taskvine-backpack
channels:
  - conda-forge
dependencies:
  - python=3.11
  - ndcctools=7.17.1
```

This file records the direct software requirements that Floability installs
and distributes to the TaskVine worker.

### 4. Request one small worker

Open the compute specification:

```bash
nano ~/tutorial/created-backpacks/my-taskvine-backpack/compute/compute.yml
```

Replace it with:

```yaml
vine_factory_config:
  min-workers: 1
  max-workers: 1
  cores: 1
  memory: 2048
  disk: 4096
```

Floability reads this file and starts one local worker for the exercise.

### 5. Validate and execute the backpack

```bash
floability backpack validate --strict \
  ~/tutorial/created-backpacks/my-taskvine-backpack
```

The command should report that the backpack is valid. Now execute it:

```bash
floability execute \
  --backpack ~/tutorial/created-backpacks/my-taskvine-backpack \
  --base-dir ~/floability-runs
```

The first run may take a few minutes while Floability creates and packs the
software environment. Near the beginning of the workflow output, the local
smoke test should show your change:

```text
[manager] worker_function smoke-test: {'input': 5, 'output': 15}
```

The distributed results should map inputs `0` through `19` to multiples of
three, ending with input `19` and output `57`. Task completion order may vary.

## Part 2: Package an existing TaskVine workflow

Use `--from-workflow` when you already have a notebook, Python script, or shell
script. The starting point here is the basic matrix program from the
TaskVine hands-on exercise:

```text
examples/taskvine/matrix-basic/matrix-basic.py
```

The original program creates its own manager and asks you to launch
`vine_factory` manually. We will leave that original example unchanged and
adapt only the copy placed in the new backpack.

### 1. Scaffold the backpack

From `~/tutorial`, run:

```bash
floability backpack init \
  --name ~/tutorial/created-backpacks/matrix-basic \
  --from-workflow examples/taskvine/matrix-basic/matrix-basic.py
```

Floability asks how to construct the software specification. Select option
`1`, then provide the environment used by the existing matrix example:

```text
Select option (1-3, default 3): 1
Path to environment.yml: examples/taskvine/matrix-basic/environment.yml
```

The matrices are defined inside the script, so enter `n` when Floability asks
whether to create a data specification:

```text
Create data.yml? (y/n, default n): n
```

The command copies the script and creates initial software and compute
specifications around it.

### 2. Connect the workflow to Floability's manager

Open the copied workflow—not the original TaskVine example:

```bash
nano ~/tutorial/created-backpacks/matrix-basic/workflow/matrix-basic.py
```

Remove the unused `getpass` import. Then find the manager-creation and
`vine_factory` instruction block at the beginning of `main()`:

```python
manager_name = f"taskvine-matrix-basic-{getpass.getuser()}-{os.getpid()}"
manager = vine.Manager(port=0, name=manager_name)

print(f"Manager name: {manager_name}")
print(f"Listening on port: {manager.port}")
print("\nIn a second terminal, activate this environment and run:")
print(
    "vine_factory -T local --min-workers=1 --max-workers=2 "
    f"--manager-name {manager_name}"
)
```

Replace that block with:

```python
manager_name = os.environ["VINE_MANAGER_NAME"]
ports_text = os.environ.get("VINE_MANAGER_PORTS", "9123,9150")
manager_ports = [
    int(value.strip())
    for value in ports_text.replace(":", ",").split(",")
    if value.strip()
]
manager = vine.Manager(manager_ports, name=manager_name)

print(f"Manager name: {manager_name}")
print(f"Listening on port: {manager.port}")
```

Floability creates a new manager name for each run and exports it through
`VINE_MANAGER_NAME`. It also exports the allowed port range through
`VINE_MANAGER_PORTS`. The workflow must use those values so that the workers
started by Floability connect to the correct manager.

### 3. Reduce the worker request

Open the generated compute specification:

```bash
nano ~/tutorial/created-backpacks/matrix-basic/compute/compute.yml
```

Replace it with:

```yaml
vine_factory_config:
  min-workers: 1
  max-workers: 1
  cores: 1
  memory: 2048
  disk: 4096
```

Do not start `vine_factory` in another terminal. Floability launches it from
this compute specification.

### 4. Validate and execute the converted workflow

```bash
floability backpack validate --strict \
  ~/tutorial/created-backpacks/matrix-basic
```

```bash
floability execute \
  --backpack ~/tutorial/created-backpacks/matrix-basic \
  --base-dir ~/floability-runs
```

A successful run finishes with the same results as the standalone TaskVine
program:

```text
Completed A x B on WORKER_ADDRESS: [[19, 22], [43, 50]]
Completed C x D on WORKER_ADDRESS: [[6, 2], [8, 4]]

Basic PythonTask matrix multiplication complete.
```

## What Floability added

For both backpacks, one `floability execute` command:

1. validates and copies the backpack into a run instance;
2. creates or reuses the declared software environment;
3. starts a local `vine_factory` using `compute.yml`;
4. supplies a matching manager name and port range to the workflow;
5. runs the Python entrypoint; and
6. records the output and cleans up the worker processes.

[**Next: Generate a backpack automatically →**](audit.md)
