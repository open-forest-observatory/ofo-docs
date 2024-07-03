# ofo-docs

Follow these steps to set up a local documentation environment for the Open Forest Observatory project using MkDocs.

### Step 1: Create a Conda Environment

First, create a new Conda environment with Python 3.10 and activate it:
```
conda create --name docs-env python=3.10
conda activate docs-env
```

### Step 2: Install MkDocs and Required Plugins
```
pip install mkdocstrings
pip install mkdocs-material
pip install mkdocs-nav-weight
pip install mkdocs-awesome-pages-plugin
pip install mkdocs-git-revision-date-localized-plugin
pip install mkdocs-git-committers-plugin
```

### Step 3: Test Locally
```
mkdocs serve
```