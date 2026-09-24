# Run Your First Backpack

**Session time:** 10 minutes

In this exercise, you will run the
[matrix-multiplication-script](https://github.com/floability-hub/matrix-multiplication-script)
backpack. The workflow runs as a Python script, so its TaskVine activity and
results appear directly in the terminal. No browser or SSH tunnel is needed.

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
cd ~/tutorial/examples/backpacks/matrix-multiplication-script
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

Clone the backpack from Floability Hub:

```bash
mkdir -p ~/tutorial/examples/backpacks
git clone https://github.com/floability-hub/matrix-multiplication-script.git \
  ~/tutorial/examples/backpacks/matrix-multiplication-script
cd ~/tutorial/examples/backpacks/matrix-multiplication-script
```

**Continue with either setup**

## 2. Inspect the backpack

List its contents:

```bash
ls
```

You should see:

```text
README.md  compute  data  software  workflow
```

## 3. Execute the workflow

Run the Python entrypoint:

```bash
floability execute \
  --backpack . \
  --entrypoint matrix-multiplication-script.py
```

Do not add `--batch-type` for this exercise. Floability launches the local
TaskVine workers described by the backpack. You do not need to start
`vine_factory` or `vine_worker` in another terminal.

The first run may take a few minutes while Floability downloads the matrix
files and prepares the backpack's Conda environment. The workflow then prints
each submitted task and each completed result directly in the terminal:

```text
[manager] Found 10 matrix files
[submit 01/45] matrix_dense_00 × matrix_dense_01
...
[manager] Submitted 45 tasks
[done 01/45] matrix_dense_00 × matrix_dense_01 = 200×200 matrix; norm=93,676.2841
...
[manager] Completed all 45 tasks
```

Task completion order may differ between runs.

## 4. Confirm success

Your run succeeded if it reached:

```text
[manager] Completed all 45 tasks
```

Floability also records the complete terminal output in the run instance's
`logs/workflow.log` file.

## What Floability handled

With one command, Floability:

1. validated and copied the backpack into an isolated run instance;
2. downloaded, verified, and cached ten matrix files;
3. created and packed the declared Conda environment;
4. launched local TaskVine workers using `compute/compute.yml`;
5. executed the Python workflow in the prepared environment; and
6. stopped the worker processes when execution finished.

Next, you will run the same scientific workload interactively from a Jupyter
notebook.

[**Next: Run your first interactive backpack →**](first-interactive-backpack.md)
