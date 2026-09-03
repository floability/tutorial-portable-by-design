# Run Your First Backpack

**Session time:** 15 minutes

In this exercise, you will deploy the **matrix-multiplication** backpack, run
its notebook, and observe its TaskVine tasks.

Start with the tutorial tools activated. Live participants use:

```bash
source /opt/tutorial/activate.sh
```

Self-managed participants use:

```bash
conda activate portable-by-design
```

## 1. Locate the backpack

### Live tutorial environment

The backpack is already available in your tutorial workspace. Do not clone
another copy on the live server.

```bash
cd ~/tutorial/examples/backpacks/matrix-multiplication
```

### Self-managed environment

Download the backpack from
[Floability Hub](https://github.com/floability-hub/matrix-multiplication):

```bash
mkdir -p ~/tutorial/examples/backpacks
git clone https://github.com/floability-hub/matrix-multiplication.git \
  ~/tutorial/examples/backpacks/matrix-multiplication
cd ~/tutorial/examples/backpacks/matrix-multiplication
```

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
creates the backpack's Conda environment. Leave this terminal open. It will
eventually print a JupyterLab URL similar to:

```text
http://localhost:REMOTE_PORT/lab?token=TOKEN
```

## 4. Open JupyterLab

### Floability is running on your own computer

Open the complete URL printed by Floability in your browser.

### Floability is running on a remote server

The Jupyter server is intentionally not exposed to the public Internet. Open a
new terminal **on your own computer** and create an SSH tunnel:

```bash
ssh -N -L 8888:localhost:REMOTE_PORT USERNAME@SERVER
```

Replace:

- `REMOTE_PORT` with the port in Floability's JupyterLab URL;
- `USERNAME` with your assigned remote username; and
- `SERVER` with your assigned server address.

Keep the tunnel terminal open. In your browser, replace the remote port in the
printed URL with local port `8888`:

```text
http://localhost:8888/lab?token=TOKEN
```

If port `8888` is already in use on your computer, choose another local port,
such as `8889`, in both the SSH command and browser URL.

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
