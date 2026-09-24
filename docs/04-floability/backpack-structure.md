# Structure of a Floability Backpack

**Session time:** 10 minutes

You have now run two versions of the matrix-multiplication workflow: a Python
script with `floability execute` and a notebook with `floability run`. This
section compares their contents and connects each directory to a deployment
responsibility.

## Learning goals

- identify the workflow entrypoint under `workflow/`;
- read the Conda specification under `software/`;
- understand data sources and integrity information under `data/`;
- read worker and resource requirements under `compute/`; and
- distinguish portable backpack requirements from site-specific choices.

## 1. Compare the two backpacks

Return to the backpack directory:

```bash
cd ~/tutorial/examples/backpacks
```

List the files in both backpacks:

```bash
find matrix-multiplication-script -maxdepth 2 -type f | sort
find matrix-multiplication -maxdepth 2 -type f | sort
```

Both use the same backpack structure:

```text
backpack/
├── compute/
│   └── compute.yml
├── data/
│   └── data.yml
├── software/
│   └── environment.yml
└── workflow/
    └── entrypoint
```

The entrypoint and execution mode differ, but the deployment responsibilities
remain in the same locations:

| Component | Script backpack | Interactive backpack |
| --- | --- | --- |
| Workflow | Python script | Jupyter notebook |
| Command | `floability execute` | `floability run` |
| Interface | Terminal output | JupyterLab |
| Software | `software/environment.yml` | `software/environment.yml` |
| Data | `data/data.yml` | `data/data.yml` |
| Compute | `compute/compute.yml` | `compute/compute.yml` |

## 2. Workflow specification

The script backpack contains a Python entrypoint:

```bash
ls matrix-multiplication-script/workflow
sed -n '1,220p' \
  matrix-multiplication-script/workflow/matrix-multiplication-script.py
```

The interactive backpack contains a notebook:

```bash
ls matrix-multiplication/workflow
```

Floability runs the Python entrypoint to completion with `execute`. With
`run`, it starts JupyterLab and lets you control the notebook interactively.
In both cases, the workflow creates a TaskVine manager and submits the matrix
tasks.

## 3. Software specification

Compare the requested Conda environments:

```bash
cat matrix-multiplication-script/software/environment.yml
cat matrix-multiplication/software/environment.yml
```

Each file records the direct software requirements for its workflow, including
Python, NumPy, and TaskVine. Floability creates the environment once, packs it
for workers, makes the prepared copy immutable, and can reuse it in later
runs.

## 4. Data specification

Inspect the beginning of each data specification:

```bash
sed -n '1,80p' matrix-multiplication-script/data/data.yml
sed -n '1,80p' matrix-multiplication/data/data.yml
```

The entries describe where each matrix comes from and where it should appear
inside the workflow directory. The script backpack also records exact file
sizes and SHA-256 checksums. Floability can download the inputs once, verify
them, cache them, and stage them into later run instances.

## 5. Compute specification

Compare the worker requests:

```bash
cat matrix-multiplication-script/compute/compute.yml
cat matrix-multiplication/compute/compute.yml
```

The compute specification records the intended worker range and the cores,
memory, and disk requested for each worker. For the tutorial, both backpacks
use small local workers.

The backpack does not hard-code the site's scheduler. A deployment can select
an available batch system at run time, for example:

```bash
floability execute --backpack matrix-multiplication-script \
  --entrypoint matrix-multiplication-script.py \
  --batch-type slurm
```

Do not run that command during the live exercise. The tutorial uses local
workers, and a Slurm deployment would require a configured Slurm site.

## The portability boundary

The backpack carries the application requirements:

```text
workflow + software + data + compute intent
```

The execution site supplies operational details such as storage locations,
network access, scheduler availability, and policy. Floability combines those
two sides when it creates a run instance.

[**Next: Create and run a backpack →**](create-backpack.md)
