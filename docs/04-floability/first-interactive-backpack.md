# Run Your First Interactive Backpack

**Session time:** 15 minutes

You just used `floability execute` to run a Python script entirely in the
terminal. In this exercise, you will deploy the notebook-based
**matrix-multiplication** backpack with `floability run`, open JupyterLab, and
observe the same TaskVine workload interactively.

```text
Script backpack       floability execute    terminal output
Notebook backpack     floability run        JupyterLab
```

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

## 1. Locate the backpack

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

The backpack is already available in your tutorial workspace. Do not clone
another copy on the live server.

```bash
cd ~/tutorial/examples/backpacks/matrix-multiplication
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

Download the backpack from
[Floability Hub](https://github.com/floability-hub/matrix-multiplication):

```bash
mkdir -p ~/tutorial/examples/backpacks
git clone https://github.com/floability-hub/matrix-multiplication.git \
  ~/tutorial/examples/backpacks/matrix-multiplication
cd ~/tutorial/examples/backpacks/matrix-multiplication
```

**Continue with either setup**

Both setup paths now use the same backpack directory.

## 2. Recognize the backpack root

List its contents:

```bash
ls
```

You should see:

```text
README.md  compute  data  software  workflow
```

These directories are the backpack's workflow, software, data, and compute
specifications. We will examine them in the next section.

For this example:

- `workflow/` contains the matrix-multiplication notebook;
- `software/` requests Python, NumPy, and TaskVine;
- `data/` declares ten public 200 by 200 matrix files; and
- `compute/` requests two to four one-core workers.

## 3. Start the backpack

Run Floability from the backpack root:

```bash
floability run --backpack .
```

Do not add `--batch-type` for this exercise. Floability will launch local
TaskVine workers on the tutorial machine. You do not need to start
`vine_factory` or `vine_worker` in another terminal; Floability manages the
workers for this backpack.

The first run may take a few minutes while Floability downloads input data and
creates the backpack's Conda environment. Leave this terminal open. When
startup finishes, Floability prints the JupyterLab URLs and, for remote access,
an SSH tunnel command.

```text
http://localhost:<REMOTE_PORT>/lab?token=<TOKEN>
```

## 4. Open JupyterLab

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

## 5. Run the workflow

In JupyterLab, open:

```text
workflow/matrix-multiplication.ipynb
```

Run the notebook cells in order. The notebook discovers ten staged matrix
files and submits one multiplication for every unique pair:

```text
10 × 9 / 2 = 45 tasks
```

A successful run completes all 45 TaskVine tasks and reports the five matrix
pairs with the largest Frobenius norms. Task completion order and worker
addresses may differ between runs.

## 6. Save and stop the run

Save the notebook in JupyterLab. Return to the terminal running Floability and
press `Ctrl-C` once:

```text
Ctrl-C
```

Floability stops JupyterLab and the worker factory, cleans up their processes,
and synchronizes the edited notebook back to the backpack. You may also close
the SSH tunnel with `Ctrl-C` after JupyterLab has stopped.

## What Floability handled

During this one command, Floability:

1. validated the backpack;
2. created an isolated run instance;
3. downloaded and cached the matrix inputs;
4. created and packed the declared software environment;
5. launched local TaskVine workers;
6. started JupyterLab inside the prepared environment; and
7. cleaned up the processes when you stopped the run.

[**Next: Structure of a backpack →**](backpack-structure.md)
