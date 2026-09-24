# Floability Overview

Floability deploys scientific workflows as portable units called
**backpacks**. A backpack keeps a workflow together with the specifications
needed to prepare its software, locate its data, and connect it to computing
resources.

This part of the tutorial begins by running the same scientific workload in
two modes: a Python script that prints results in the terminal and an
interactive notebook served through JupyterLab. You will then compare their
backpack structures, create a backpack, and generate initial specifications
from an observed notebook execution.

## Floability sessions

| Time | Session | What you will do |
| ---: | --- | --- |
| 10 min | Floability overview | Understand the deployment problem and backpack model |
| 10 min | [Run your first backpack](first-backpack.md) | Execute a Python workflow and watch its results in the terminal |
| 15 min | [Run your first interactive backpack](first-interactive-backpack.md) | Run the same workload from a notebook through JupyterLab |
| 10 min | [Structure of a backpack](backpack-structure.md) | Compare their workflow, software, data, and compute specifications |
| 15 min | [Create and run a backpack](create-backpack.md) | Package a workflow and run the resulting backpack |
| 10 min | [Generate a backpack automatically](audit.md) | Use Audit to create initial specifications from a working notebook environment |
| 5 min | Wrap-up and questions | Review the portability model and next steps |

## The backpack model

```text
my-backpack/
├── workflow/       notebook, Python script, or shell entrypoint
├── software/       Conda environment specification
├── data/           data sources, profiles, and integrity information
└── compute/        worker and resource requirements
```

The specifications are explicit and reviewable. Floability uses them to stage
data, prepare and cache software environments, create an isolated run instance,
launch TaskVine workers, and start the workflow interactively or execute it
without a browser.

The goal is not to hide every site difference. The goal is to keep the
application's portable requirements with the workflow while allowing
site-specific storage, scheduler, network, and policy settings to be supplied
at deployment time.

[**Run your first backpack →**](first-backpack.md)

## After the tutorial

The live schedule uses the matrix example. If you want a more advanced
workflow afterward, continue with
[**MobileNet batch inference**](optional-backpacks/mobilenet.md) or browse the
[complete collection in Floability Hub](https://github.com/floability-hub).
