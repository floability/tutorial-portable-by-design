# Create Your Own Environment

<span class="tutorial-route-badge tutorial-route--self-managed">Self-managed</span>

Use this setup if you are following the tutorial on your own x86-64 Linux computer or server.

You need:

- Linux.
- x86-64 architecture.
- Conda or Miniforge.
- Git.

If Conda is not installed, install [Miniforge](https://github.com/conda-forge/miniforge) before continuing.

## 1. Clone the tutorial repository

Clone the repository into the standard tutorial location:

```bash
git clone https://github.com/floability/tutorial-portable-by-design.git ~/tutorial
cd ~/tutorial
```

The repository contains the tutorial instructions, scripts, and examples. Run the remaining setup commands from the repository root.

## 2. Create the tutorial environment

Run:

```bash
conda create -y -n tutorial-env \
  -c conda-forge \
  --strict-channel-priority \
  python=3.11 \
  pip \
  git \
  jupyterlab \
  ndcctools=7.17.1 \
  floability=0.3.0 \
  cloudpickle=3.1.2 \
  numpy=2.4.3 \
  pandas \
  matplotlib \
  onnxruntime=1.28.0 \
  pillow=12.1.1
```

Activate it:

```bash
conda activate tutorial-env
```

Install Sciunit inside the active environment:

```bash
python -m pip install --upgrade sciunit2
```

The RAG-Lite exercise intentionally uses a separate environment containing its
application dependencies. Keeping those packages out of `tutorial-env` lets
you demonstrate that Sciunit can repeat a captured execution without them
being installed in the active environment.

Whenever you open a new terminal and return to the tutorial, activate it again:

```bash
conda activate tutorial-env
```

## 3. Check the installation

Run:

```bash
python --version
vine_worker --version
sciunit --version
python -c "from sciunit2.command.exec_ import ExecCommand; print('Sciunit: OK')"
python -c "import ndcctools.taskvine; print('TaskVine: OK')"
python -c "import cloudpickle, matplotlib, numpy, onnxruntime, pandas; from PIL import Image; print('Scientific examples: OK')"
floability --help >/dev/null && echo "Floability: OK"
python -m pip check
```

You should finish with:

```text
Sciunit: OK
TaskVine: OK
Scientific examples: OK
Floability: OK
No broken requirements found.
```

## 4. Understand the environment layout

The `tutorial-env` environment contains the same participant-facing package set
as the live AWS environment. It supports the TaskVine, matrix, MobileNet,
Sciunit, and Floability exercises. The RAG-Lite Sciunit exercise creates a
separate `raglite-sciunit-env` for its application dependencies, then returns
to `tutorial-env` to demonstrate dependency-free replay.

During later exercises, Floability may create additional software environments for individual backpacks. Those environments are separate from this tutorial tools environment and may be cached for reuse.

The self-managed exercises use **directly launched TaskVine workers**. A Slurm installation is not required.

## You are ready

Continue to [**TaskVine Quickstart**](../02-taskvine/quickstart.md).
