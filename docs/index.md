# Portable by Design

## Deploying Notebook-based Scientific Workflows Across HPC Clusters

Scientific workflows can be difficult to reproduce and move between high-performance computing (HPC) systems. Software stacks differ, data may live in site-specific locations, and each cluster exposes its own resources and execution environment.

This hands-on tutorial introduces three complementary open-source tools—**TaskVine**, **Sciunit**, and **Floability**—for addressing these challenges. You will build a distributed workflow with TaskVine, capture a reproducible execution with Sciunit, and deploy a portable notebook-based workflow as a Floability backpack.

Short presentations introduce each concept, followed immediately by guided exercises that put it into practice.

## Tutorial at a glance

- **Format:** short presentations and guided hands-on exercises
- **Duration:** 3 hours total, including a 15-minute break
- **Tools:** TaskVine, Sciunit, and Floability
- **Setup:** prepared tutorial server or a self-managed x86-64 Linux system

## Tutorial outline

### Part I — TaskVine and Sciunit · 90 minutes

| Time | Topic | Materials |
| ---: | --- | --- |
| 10 min | **TaskVine overview** — manager-worker execution, dynamic scheduling, and data-intensive workflows | Slides *(coming soon)* · [Overview](02-taskvine/index.md) |
| 15 min | **Access, setup, and TaskVine quickstart** | [Setup](01-access-and-setup/index.md) · [Hands-on](02-taskvine/quickstart.md) |
| 35 min | **TaskVine application structure and execution** — tasks, files, workers, and result collection | Slides *(coming soon)* · [Hands-on](02-taskvine/matrix-files.md) |
| 30 min | **Reproducible execution with Sciunit** — capture, inspect, and reproduce an execution | Slides *(coming soon)* · [Hands-on](03-sciunit/index.md) |

### Break · 15 minutes

### Part II — Floability · 75 minutes

| Time | Topic | Materials |
| ---: | --- | --- |
| 15 min | **Floability overview** — portable notebook workflows and the backpack model | Slides *(coming soon)* |
| 20 min | **Running a basic backpack** | [Hands-on](04-floability/index.md) *(coming soon)* |
| 20 min | **Structure of a Floability backpack** — workflow, software, data, and compute specifications | Slides *(coming soon)* · [Hands-on](04-floability/index.md) *(coming soon)* |
| 20 min | **Managing data dependencies across HPC sites** — resolving, staging, verifying, and reusing data | Slides *(coming soon)* · [Hands-on](04-floability/index.md) *(coming soon)* |

## How the tools fit together

**TaskVine** provides the distributed execution layer. A manager creates tasks, workers obtain those tasks dynamically, and TaskVine moves required files and returns results.

**Sciunit** captures an execution and its dependencies so that it can be inspected and reproduced outside the original environment.

**Floability** packages a workflow with its software, data, and compute specifications in a portable deployment unit called a **backpack**. It prepares the execution environment and connects the workflow to computing resources through TaskVine.

## What you will learn

By the end of the tutorial, you will be able to:

- build and execute a distributed workflow with TaskVine;
- explain TaskVine's manager-worker execution model;
- capture and reproduce a workflow execution with Sciunit;
- run a notebook workflow packaged as a Floability backpack;
- identify the workflow, software, data, and compute specifications in a backpack; and
- manage data dependencies when moving workflows between computing environments.

## Related resources

- [TaskVine documentation](https://cctools.readthedocs.io/en/stable/taskvine/)
- [Sciunit](https://github.com/radiant-systems-lab/sciunit)
- [Floability documentation](https://floability.readthedocs.io/)
- [Floability Hub](https://github.com/floability-hub)

## Ready to begin?

Start by connecting to the prepared tutorial environment or setting up the exercises on your own Linux system.

[**Go to Access and Setup →**](01-access-and-setup/index.md)
