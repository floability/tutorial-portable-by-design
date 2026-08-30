# Create Your Own Environment

Use this setup if you are following the tutorial on your own x86-64 Linux computer or server.

You need:

- Linux.
- x86-64 architecture.
- Conda or Miniforge.
- Git.

If Conda is not installed, install [Miniforge](https://github.com/conda-forge/miniforge) before continuing.

## 1. Create the tutorial environment

Run:

```bash
conda create -y -n portable-by-design \
  -c conda-forge \
  --strict-channel-priority \
  python=3.11 \
  pip \
  git \
  jupyterlab \
  ndcctools \
  floability
```

Activate it:

```bash
conda activate portable-by-design
```

Install the Sciunit command-line tool inside the active environment:

```bash
python -m pip install sciunit2
```

Whenever you open a new terminal and return to the tutorial, activate it again:

```bash
conda activate portable-by-design
```

## 2. Check the installation

Run:

```bash
python --version
vine_worker --version
sciunit --version
python -c "import ndcctools.taskvine; print('TaskVine: OK')"
floability --help >/dev/null && echo "Floability: OK"
```

You should finish with:

```text
TaskVine: OK
Floability: OK
```

## 3. Understand the environment layout

The `portable-by-design` environment contains the tools needed to follow the tutorial.

During later exercises, Floability may create additional software environments for individual backpacks. Those environments are separate from this tutorial tools environment and may be cached for reuse.

The self-managed exercises use **directly launched TaskVine workers**. A Slurm installation is not required.

## You are ready

Continue to [**Your First TaskVine Program**](../02-taskvine/README.md).
