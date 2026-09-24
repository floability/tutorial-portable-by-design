# Generate a Backpack Automatically

**Session time:** 10 minutes

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

Check which Conda environment is active:

```bash
echo "${CONDA_PREFIX:-No Conda environment is active}"
```

The path should end in `/tutorial-env`. If it does not, activate the environment for your setup.

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

```bash
source /opt/tutorial/activate.sh
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

```bash
conda activate tutorial-env
```

**Continue with either setup**

The environment supplied to `floability audit` must already contain the dependencies required to run the notebook successfully. The tutorial environment includes NumPy, pandas, Matplotlib, and TaskVine for this notebook.

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

Before running the audit, let's determine your **manager port** from your assigned **username**.

> ⚠️ **Important: Use your own manager port**
>
> **Each user must use a different manager port to avoid conflicts when running the tutorial concurrently.**
>
> Add the **numeric part** of your **username** to **9123**.
>
> **Examples:**
>
> - `user03` → `9123 + 3 = 9126`
> - `user11` → `9123 + 11 = 9134`
>
> ⚠️ **Replace `<MANAGER_PORT>` in the command below with your calculated port number.**

Now run:

```bash
floability audit \
    --notebook matrix-multiplication.ipynb \
    --conda-env "$CONDA_PREFIX" \
    --data-dirs ./data \
    --manager-port <MANAGER_PORT> \
    --backpack-name matrix-backpack
```

The important options are:

| Option | What it does |
| --- | --- |
| `--notebook` | Specifies the notebook to execute and audit |
| `--conda-env` | Specifies the working Conda environment |
| `--data-dirs` | Tells Audit where possible input data files are located |
| `--manager-port` | Assigns this participant a unique local manager port |
| `--backpack-name` | Sets the name of the generated backpack |

There are several additional options that you can check using `floability audit -h`.

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

## 5. Run the Backpack

Run the backpack interactively:

```bash
floability run --backpack matrix-backpack
```

Floability uses the generated specifications to prepare the workflow and launch JupyterLab.

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

Floability is running on your own computer. Open the complete URL printed by
Floability in your browser.

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

Floability is running on a remote server. The Jupyter server is intentionally
not exposed to the public Internet. Open a new terminal **on your own
computer** and create an SSH tunnel:

!!! important "Floability prints a ready-to-copy command"

    When startup finishes, Floability prints the complete SSH tunnel command
    with the correct server address and port. You can copy and run that command
    directly. The pattern below is available if you need to enter it manually.

```bash
ssh -N -L 8888:localhost:<REMOTE_PORT> <USERNAME>@<SERVER>
```

Replace:

- `<REMOTE_PORT>` with the port in Floability's JupyterLab URL;
- `<USERNAME>` with your assigned remote username; and
- `<SERVER>` with your assigned server address.

Keep the tunnel terminal open. In your browser, replace the remote port in the
printed URL with local port `8888`:

```text
http://localhost:8888/lab?token=<TOKEN>
```

If port `8888` is already in use on your computer, choose another local port,
such as `8889`, in both the SSH command and browser URL.

**Continue with either setup**

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

[**Next: Optional backpack examples →**](optional-backpacks/index.md)
