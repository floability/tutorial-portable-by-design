# Generate a Backpack Automatically

**Session time:** 15 minutes

> **You already have a Jupyter notebook that works. But how do you turn it into a Floability Backpack without manually specifying all of its software and data dependencies?**




```text
👨‍💻 Notebook User

"I already have a working notebook.
How do I generate a Backpack from it?"

                ↓

📓 Notebook  +  🐍 Environment  +  📁 Input Data

                ↓

         floability audit

                ↓

       🎒 Floability Backpack
```

For `floability audit` to work, you should already have:

- a **working Jupyter notebook**;
- the **Conda environment** in which the notebook runs successfully; and
- the notebook's required **input data files** available locally.

Then `floability audit` can observe the notebook while it runs and generate an initial backpack for you.

Instead of manually identifying every software dependency and input file, `floability audit` executes the notebook and observes what it actually uses.

> **Important:** Audit does not create the notebook's environment or recover missing input data. The notebook must already run successfully with its required environment and input files available. Audit is currently experimental, so the generated backpack should be reviewed and tested before being shared or used for larger runs.


<!--
## Learning goals

By the end of this tutorial, you will be able to:

- run Floability Audit on an existing working notebook;
- understand what Audit observes during execution;
- inspect the generated software, data, workflow, and compute specifications; and
- validate and run the generated backpack.

In this tutorial, we will use a [Matrix Multiplication notebook](https://github.com/floability/tutorial-portable-by-design/blob/main/examples/audit/matrix-multiplication.ipynb).
-->

---

## 1. Before we begin

First, activate the correct environment for this demo

```bash
source /opt/tutorial/activate-matrix.sh
```
Let's verify if we are in the correct environment.

```bash
echo "${CONDA_PREFIX:-No Conda environment is active}"
```

The path should end in:

```text
/matrix-env
```

If it does not, activate the tutorial environment.


```bash
conda activate matrix-env
```

The environment supplied to  `floability audit` must already contain the dependencies required to run the notebook successfully.

---

## 2. Check the Notebook and Input Data availability

Navigate to the audit example directory:

```bash
cd ~/tutorial/examples/audit
```

Check its contents:

```bash
ls -lahtr
```

You should see the [matrix multiplication](https://github.com/floability/tutorial-portable-by-design/blob/main/examples/audit/matrix-multiplication.ipynb) notebook and a `data` directory.

Now inspect the input data:

```bash
ls -lahtr data/matrices
```
You should see some csv files.

If the above are available, then the example is already set up with everything `floability audit` needs:

```text
audit/
├── matrix-multiplication.ipynb
└── data/
    └── matrices/
        └── input matrix files
```

At this point, we have the three things needed for an audit:

```text
📓 Working notebook
        +
🐍 Working Conda environment
        +
📁 Available input data
        ↓
   floability audit
```

---

## 3. Run Floability Audit

Now run:

```bash
floability audit \
    --notebook matrix-multiplication.ipynb \
    --conda-env "$CONDA_PREFIX" \
    --data-dirs ./data \
    --backpack-name matrix-backpack
```

The important options are:

| Option | What it does |
| --- | --- |
| `--notebook` | Specifies the notebook to execute and audit |
| `--conda-env` | Specifies the working Conda environment |
| `--data-dirs` | Tells Audit where possible input data files are located |
| `--backpack-name` | Sets the name of the generated backpack |

There are several additional options that you can check using `floability audit -h`

During the audit, Floability executes the notebook and observes the dependencies used during that execution.

Instead of manually specifying things, Floability collects this information from the execution and uses it to create an initial backpack.

---

## 4. Inspect the Generated Backpack

After the audit finishes, check the generated backpack:

```bash
ls -lahtr matrix-backpack
```

The generated directory will have a structure similar to:

```text
matrix-backpack/
├── compute/
│   └── compute.yml
├── data/
│   └── data.yml
├── software/
│   └── environment.yml
└── workflow/
    └── matrix-multiplication.ipynb
```

The main files are:

- `workflow/matrix-multiplication.ipynb` — the notebook
- `software/environment.yml` — discovered software dependencies
- `data/data.yml` — detected input data
- `compute/compute.yml` — initial compute configuration

For example, inspect the generated software specification:

```bash
cat matrix-backpack/software/environment.yml
```

Then inspect the detected data:

```bash
cat matrix-backpack/data/data.yml
```

---

## 5. Validate the Backpack

Check that the generated backpack has a valid Floability structure:

```bash
floability backpack validate matrix-backpack
```

---

## 6. Run the Backpack

Run the backpack interactively:

```bash
floability run --backpack matrix-backpack
```

Floability uses the generated specifications to prepare the workflow and launch JupyterLab.

You can also execute the notebook without opening Jupyter:

```bash
floability execute --backpack matrix-backpack
```

For a Slurm cluster:

```bash
floability run \
    --backpack matrix-backpack \
    --batch-type slurm
```

---

## What Did We Do?

We started with an existing working notebook setup:

```text
📓 Notebook  +  🐍 Environment  +  📁 Input Data
                ↓
         floability audit
                ↓
       🎒 Generated Backpack
```

Instead of manually specifying everything the notebook requires, we let Floability observe a successful execution and generate the initial backpack specifications.

<!--

The key point is:

> **Audit helps turn an already working notebook into a backpack. It does not make a broken or incomplete notebook environment work automatically.**

From here, you can review the generated specifications, validate the backpack, and use it to reproduce the workflow on another supported system.
Instead of manually identifying every software dependency and input file, `floability audit` executes the notebook and observes what it actually uses.

> **Important:** Audit does not create the notebook's environment or recover missing input data. The notebook must already run successfully with its required environment and input files available.

Audit is currently experimental, so the generated backpack should be reviewed and tested before being shared or used for larger runs.



## Learning goals

By the end of this tutorial, you will be able to:

- run Floability Audit on an existing working notebook;
- understand what Audit observes during execution;
- inspect the generated software, data, workflow, and compute specifications; and
- validate and run the generated backpack.

In this tutorial, we will use a [Matrix Multiplication notebook](https://github.com/floability/tutorial-portable-by-design/blob/main/examples/audit/matrix-multiplication.ipynb).

[**Return to the Floability overview →**](index.md)

---

## 1. Check Your Environment

First, check which Conda environment is currently active:

```bash
echo "${CONDA_PREFIX:-No Conda environment is active}"
```

The path should end in:

```text
/tutorial-env
```

If it does not, activate the tutorial environment.

### Live tutorial

```bash
source /opt/tutorial/activate.sh
```

### Self-managed setup

```bash
conda activate tutorial-env
```

The environment supplied to Audit must already contain the dependencies required to run the notebook successfully.

---

## 2. Check the Notebook and Input Data

Navigate to the audit example directory:

```bash
cd ~/tutorial/examples/audit
```

Check its contents:

```bash
ls -lah
```

You should see the matrix multiplication notebook and a `data` directory.

Now inspect the input data:

```bash
ls -lah data/matrices
```

The example is already set up with everything Audit needs:

```text
audit/
├── matrix-multiplication.ipynb
└── data/

[**Return to the Floability overview →**](index.md)
