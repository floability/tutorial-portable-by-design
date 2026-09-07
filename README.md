# Portable by Design Tutorial

Hands-on materials for **Portable by Design: Deploying Notebook-based Scientific Workflows across HPC Clusters**.

This tutorial introduces tools and techniques for building portable, reproducible scientific workflows using **TaskVine, Sciunit, and Floability**. The repository contains the instructions and runnable exercises needed to follow the tutorial.

## Getting Started

Start with **[Access and Setup](docs/01-access-and-setup/index.md)**.

You can follow the tutorial in either of two ways:

* **Live tutorial participant** — connect to the prepared tutorial server using the credentials provided during the session.
* **Self-managed setup** — create the tutorial environment on your own Linux computer or server.

## Tutorial Materials

* **Slides** — coming soon.
* **TaskVine exercises** — coming soon.
* **Sciunit exercises** — coming soon.
* **Floability exercises** — coming soon.

## Preview the documentation locally

Create a documentation-only Python environment:

```bash
python3 -m venv .venv-docs
source .venv-docs/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-docs.txt
```

Start the development server:

```bash
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). MkDocs automatically rebuilds the site when a documentation file changes. Stop the server with `Ctrl+C`.

For later preview sessions, reactivate the environment and restart MkDocs:

```bash
source .venv-docs/bin/activate
mkdocs serve
```

Before committing documentation changes, run the strict build check:

```bash
mkdocs build --strict
```

## Update the GitHub Pages site

Pushing changes to `main` does not update the published website. Continue developing and committing normally, and deploy only when the documentation is ready to be published.

When you are ready to publish, make sure the desired changes are committed and run:

```bash
mkdocs build --strict
mkdocs gh-deploy
```

The first deployment creates the `gh-pages` branch. In the GitHub repository, open **Settings → Pages**, select **Deploy from a branch**, choose the `gh-pages` branch and `/ (root)`, and click **Save**.

The site will be available at [https://floability.github.io/tutorial-portable-by-design/](https://floability.github.io/tutorial-portable-by-design/). Do not edit the `gh-pages` branch directly; update the Markdown source and run `mkdocs gh-deploy` again.
