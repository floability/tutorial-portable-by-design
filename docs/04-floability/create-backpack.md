# Create and Run Your Own Backpack

**Session time:** 15 minutes

For most existing notebooks, Python scripts, and shell scripts, you can ask
Floability to create the backpack scaffold around the workflow. You then
review its specifications and make any changes required for Floability-managed
execution.

See the official
[Create Your First Backpack](https://floability.readthedocs.io/en/stable/getting-started/create-first-backpack/)
guide for every creation method and command-line option.

## Start from a template

If you want a starting point that you can customize and build on, use
Floability's template feature. Templates create a Jupyter notebook by default.

The recommended path below creates a notebook with managed input data. The
alternative creates a simpler Python script without managed data. Choose one,
inspect the generated backpack, make a small change, and run it.

## Before you begin

Check which Conda environment is active:

```bash
echo "${CONDA_PREFIX:-No Conda environment is active}"
```

The path should end in `/tutorial-env`. If it does not, activate the tutorial
environment using the command for your setup:

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

```bash
source /opt/tutorial/activate.sh
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

```bash
conda activate tutorial-env
```

**Continue with either setup**

Create a location for the backpack:

```bash
mkdir -p ~/tutorial/created-backpacks
```

## 1. Create a backpack

Run **one** of the following commands—not both.

### Notebook with managed data

```bash
floability backpack init \
  --name ~/tutorial/created-backpacks/my-taskvine-backpack \
  --from-template taskvine-data
```

This is the default notebook-based path. It creates a TaskVine notebook,
`data/data.yml`, one backpack-local text file, and one remote text input.

### Script without managed data

```bash
floability backpack init \
  --name ~/tutorial/created-backpacks/my-taskvine-backpack \
  --from-template taskvine \
  --script
```

The `--script` option creates a Python entrypoint. This basic template leaves
input-data management to the workflow, so it does not create `data/data.yml`.

## 2. Inspect the generated backpack

```bash
find ~/tutorial/created-backpacks/my-taskvine-backpack \
  -maxdepth 3 -type f | sort
```

Both options include:

```text
my-taskvine-backpack/
├── compute/
│   └── compute.yml
├── software/
│   └── environment.yml
└── workflow/
    └── my-taskvine-backpack.py or my-taskvine-backpack.ipynb
```

The notebook option also includes:

```text
data/
├── data.yml
└── text_data/
    └── local-sample.txt
```

## 3. Set the software specification

Use the same pinned software specification as the matrix backpack you ran
earlier:

```bash
cp ~/tutorial/examples/backpacks/matrix-multiplication-script/software/environment.yml \
  ~/tutorial/created-backpacks/my-taskvine-backpack/software/environment.yml
cat ~/tutorial/created-backpacks/my-taskvine-backpack/software/environment.yml
```

The starter workflows do not require NumPy, but using the identical
specification allows Floability to reuse the environment prepared by the
matrix exercise. If you skipped that exercise, Floability creates the
environment now.

## 4. Request one small worker

Open the compute specification:

```bash
nano ~/tutorial/created-backpacks/my-taskvine-backpack/compute/compute.yml
```

Replace its contents with:

```yaml
vine_factory_config:
  min-workers: 1
  max-workers: 1
  cores: 1
  memory: 2048
  disk: 4096
```

Save with `Ctrl-O`, press `Enter`, and exit with `Ctrl-X`. Floability will use
this file to start one local worker.

## 5. Customize the workflow

### If you created the notebook

Continue to the next step. After JupyterLab opens, find the cell defining:

```python
def worker_function(file_path, keywords=("war", "peace")):
```

Add `"love"` to the keyword tuple, then run all cells:

```python
def worker_function(file_path, keywords=("war", "peace", "love")):
```

### If you created the script

Open the generated Python file:

```bash
nano ~/tutorial/created-backpacks/my-taskvine-backpack/workflow/*.py
```

Find:

```python
return {"input": value, "output": value * 2}
```

Change the multiplier from `2` to `3`, then save and exit. The output should
now contain multiples of three.

## 6. Run the backpack

Use the command that matches the workflow type you generated.

### Notebook entrypoint

```bash
floability run \
  --backpack ~/tutorial/created-backpacks/my-taskvine-backpack
```

Floability prints the JupyterLab URL and, for a remote server, the SSH tunnel
command. Open JupyterLab, select the generated notebook, add `"love"` to the
keyword tuple, and run all cells. The workflow should process two staged text
files. Stop the Floability process with `Ctrl-C` when you are finished.

!!! important "Floability prints a ready-to-copy command"

    Live participants can copy the complete SSH tunnel command printed by
    Floability. Use the same JupyterLab access process as in
    [Run Your First Interactive Backpack](first-interactive-backpack.md#4-open-jupyterlab).

### Script entrypoint

```bash
floability execute \
  --backpack ~/tutorial/created-backpacks/my-taskvine-backpack
```

The workflow runs to completion and prints its results in the terminal. The
last line should report that all 20 tasks completed.

## What Floability added

For the backpack you created, Floability:

1. created a standard backpack structure;
2. supplied a workflow that connects to its TaskVine manager;
3. created initial software and compute specifications;
4. created a managed-data specification for the notebook option;
5. prepared or reused the software environment;
6. launched the requested local worker; and
7. ran either a script or an interactive notebook.

## Reset

To repeat this exercise with the other option, remove only the backpack you
created, then return to step 1:

```bash
test -d "$HOME/tutorial/created-backpacks/my-taskvine-backpack"
rm -rf -- "$HOME/tutorial/created-backpacks/my-taskvine-backpack"
```

## Start from an existing workflow

Use `--from-workflow` when you already have working code:

```bash
floability backpack init \
  --name ~/tutorial/created-backpacks/my-existing-workflow \
  --from-workflow /path/to/my-workflow.ipynb
```

Floability copies the entrypoint and creates the surrounding scaffold:

```text
my-existing-workflow/
├── compute/
│   └── compute.yml
├── data/
│   └── data.yml             optional
├── software/
│   └── environment.yml
└── workflow/
    └── my-workflow.ipynb    or a Python or shell script
```

Review every generated specification. The software file must contain the
workflow's direct dependencies, the compute file must describe suitable
workers, and `data.yml` must identify any inputs Floability should stage.

### Connect an existing TaskVine workflow

A standalone TaskVine application may create an arbitrary manager name and
port, then ask you to start a worker or factory manually. Inside a backpack,
Floability chooses the manager name and allowed port range so that the workers
it launches can find the workflow.

Read those values from the environment when creating the manager:

```python
import os
import ndcctools.taskvine as vine

manager_name = os.environ["VINE_MANAGER_NAME"]
ports_text = os.environ.get("VINE_MANAGER_PORTS", "9123,9150")
manager_ports = [
    int(value.strip())
    for value in ports_text.replace(":", ",").split(",")
    if value.strip()
]

manager = vine.Manager(manager_ports, name=manager_name)
```

Remove instructions that launch `vine_worker` or `vine_factory` manually.
Floability starts the workers from `compute/compute.yml`.

[**Next: Generate a backpack automatically →**](audit.md)
