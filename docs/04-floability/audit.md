# Generate a Backpack Automatically

**Session time:** 15 minutes

Floability Audit observes a notebook running in an accessible Conda
environment and generates initial backpack specifications. Audit is an
experimental starting point, not a replacement for reviewing and testing the
resulting backpack.

## Learning goals

- recognize when Audit is appropriate;
- run Audit against a notebook that already executes successfully;
- inspect the generated workflow, software, data, and compute files;
- understand which dependencies Audit cannot infer reliably; and
- edit and validate the generated backpack before sharing it.

The final exercise will use a small notebook with a known-good local Conda
environment so participants can focus on inspecting the generated result.

[**Return to the Floability overview →**](index.md)

# Create a Backpack Automatically with Floability Audit

If you already have a Jupyter notebook that runs successfully, Floability can help create a backpack automatically.

Instead of manually writing the software and data specifications, `floability audit` runs the notebook, observes the software and input files it uses, and generates an initial backpack for you.

In this tutorial, we will use a [Matrix Multiplication notebook](https://github.com/floability/tutorial-portable-by-design/blob/main/examples/audit/matrix-multiplication.ipynb).

> `floability audit` is currently experimental. The generated backpack should be reviewed before using it for larger runs.

## Before you begin

Check which Conda environment is active:

```bash
echo "${CONDA_PREFIX:-No Conda environment is active}"
```

The path should end in `/tutorial-env`. If it does not, activate the tutorial
environment using the command for your setup:

### Live tutorial

```bash
source /opt/tutorial/activate.sh
```

### Self-managed

```bash
conda activate tutorial-env
```

## 1. Get the Example Notebook

Clone the matrix multiplication example:

```bash
git clone https://github.com/floability-hub/matrix-multiplication.git
```

The notebook is located at:

```text
matrix-multiplication/workflow/matrix-multiplication.ipynb
```

You can keep the notebook wherever you normally work. The notebook does **not** need to be inside the directory where you want the new backpack to be created.

---

## 2. Activate the Notebook Environment

The notebook must already run successfully in a Conda environment.

Activate that environment:

```bash
conda activate my-env
```

Find its environment prefix:

```bash
echo $CONDA_PREFIX
```

For example:

```text
/home/user/miniconda3/envs/my-env
```

Floability uses this environment while auditing the notebook.

---

## 3. Run the Audit

Now run:

```bash
floability audit \
    --notebook /path/to/matrix-multiplication/workflow/matrix-multiplication.ipynb \
    --conda-env "$CONDA_PREFIX" \
    --data-dirs /path/to/matrix-multiplication/data \
    --backpack-name matrix-backpack
```

The important options are:

| Option | What it does |
| --- | --- |
| `--notebook` | Path to the notebook you want to audit |
| `--conda-env` | Conda environment used to run the notebook |
| `--data-dirs` | Directories containing possible input data |
| `--backpack-name` | Name of the backpack to create |

During the audit, Floability executes the notebook and traces the dependencies it actually uses. It captures Python software dependencies and looks for input files accessed from the directories supplied with `--data-dirs`. For TaskVine notebooks, it also traces the worker execution separately. :contentReference[oaicite:1]{index=1}

---

## 4. Check the Generated Backpack

After the audit completes, Floability creates:

```text
matrix-backpack/
├── compute/
│   └── compute.yml
├── data/
│   ├── data.yml
│   └── ...
├── software/
│   └── environment.yml
└── workflow/
    └── matrix-multiplication.ipynb
```

The main files are:

- `workflow/matrix-multiplication.ipynb` — your notebook
- `software/environment.yml` — software dependencies discovered during execution
- `data/data.yml` — detected input data
- `compute/compute.yml` — starting worker/resource configuration

Audit observes a particular execution, so these files should be checked before running the backpack. In particular, verify the software dependencies, detected data files, and worker resource settings. :contentReference[oaicite:2]{index=2}

---

## 5. Validate the Backpack

Check that the generated backpack has a valid Floability structure:

```bash
floability backpack validate matrix-backpack
```

---

## 6. Run the Backpack

Run it interactively with:

```bash
floability run --backpack matrix-backpack
```

Floability prepares the software environment, stages the required data, starts the TaskVine workers, and launches JupyterLab.

For a Slurm cluster:

```bash
floability run \
    --backpack matrix-backpack \
    --batch-type slurm
```

Or execute the notebook without opening Jupyter:

```bash
floability execute --backpack matrix-backpack
```

For the matrix multiplication example, the notebook distributes matrix-pair computations as independent TaskVine tasks. :contentReference[oaicite:3]{index=3}

---

## What Did We Do?

We started with only a working notebook and its existing environment:

```text
Notebook + Conda environment + input data
                    |
                    v
             floability audit
                    |
                    v
          Floability Backpack
```

Instead of manually identifying every dependency, Floability observed the notebook execution and generated the initial backpack specifications automatically.

From here, you can review the backpack and run the same workflow locally or on a supported HPC system.
