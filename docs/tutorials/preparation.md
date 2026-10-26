---
weight: 1
---

# Preparing to follow the tutorials

The information here applies to all OFO tutorials. Follow the guidance here before starting any of the tutorials.

## Example input data

For all tutorial data processing tasks, we provide example input data you can use (though you can alternatively use your own data). If you will use the example data, we recommend you download the entire folder of example data in advance, as its file tree matches the expectations of the example code in the tutorials. We recommend downloading the example data to a folder named `ofo-tutorial-data` in your home directory.

[:material-download: Download example data](https://ucdavis.box.com/s/iq6afom3pxg81y8vts8imidy3a91fvoy) (4.6 GB)

Alternatively, you can download just the input data needed for a specific tutorial task (linked in an "input data" table near the top of each tutorial task page). In that case, you may need to modify the input file paths in the example code more extensively to match the location of the input data on your computer.

## Setting the `DATA_DIR` environment variable

Before running any of the tutorials, you will need to set an environment variable, `DATA_DIR`, that the example code looks for in order to find the input data. Run this line in every new terminal window where you will run the tutorial code. Adjust the path below to match the location of the example data on your computer.

=== "Linux/Mac"

    ```bash
    export DATA_DIR="~/ofo-tutorial-data"
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:DATA_DIR = "$HOME\ofo-tutorial-data"
    ```

By default, the tutorial exercises will save output data to an `outputs` folder at the top level of this directory.


## Computing hardware requirements

For processing a single drone mission at a time (up to ~50 ha), a standard laptop or desktop computer is generally sufficient, though computer vision inference tasks will generally be much faster if a GPU is available.

## Docker

!!! question "Should I use Docker?"

    OFO tools are written in Python, and they require some work to install. Docker is an alternative to running Python code directly that minimizes installation complexity. However, running Python code directly affords more flexibility and control. If you wish to run OFO tools using Python directly, skip to the [Native Python](#native-python) section below.

Docker is a system that allows software developers to distribute software packages, including all their dependencies, in a way that can be run on any operating system. For each OFO tool, OFO provides a Docker *image*, which essentially contains the software (Python code), its dependencies, and a minimal operating system. When you run an instance of a Docker image on your computer, it is called a *container*.

Docker provides a convenient way for users to run OFO software without having to run any Python code directly, or worry about installing Python libraries and other dependencies. When users run OFO tools using Docker, they run a single command in a terminal window. This command specifies the Docker image to use, the input and output file locations, and the processing parameters. A docker command might look like the following (in this case for detecting trees from a canopy height model using the OFO [Tree Detection Framework]):

=== "Linux/Mac"

    ```bash
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "path/to/local/data:/data/in/container" \
        ghcr.io/open-forest-observatory/tree-detection-framework \
        python -m tree_detection_framework.entrypoints.detect_geometric_two_stage \
            /data/drone/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
            /data/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
            --raster-blur-sigma 0.5
    ```

=== "Windows (PowerShell)"

    ```powershell
    docker run --rm `
        -v "path\to\local\data:/data/in/container" `
        ghcr.io/open-forest-observatory/tree-detection-framework `
        python -m tree_detection_framework.entrypoints.detect_geometric_two_stage `
            /data/drone/photogrammetry-postprocessed/full/composite1_chm-mesh.tif `
            /data/detected-trees/composite1_tree-tops_geometric_v01.gpkg `
            --raster-blur-sigma 0.5 `
    ```

This command downloads the `tree-detection-framework` Docker image (if it is not already downloaded), runs the software in the image, and saves the output files to your computer. The `-v` option specifies a folder on your computer that is made available to the software running in the Docker container, which sees it at the path following the `:`. In this case, the folder `path/to/local/data` on your computer is made available as `/data/in/container` inside the container. The input and output file paths are specified relative to this folder.

To be able to run Docker containers, you need to install Docker on your computer.


### Install Docker

Below are the minimal instructions for installing Docker on Linux, Mac, or Windows. For more detailed instructions, see the [Docker documentation](https://docs.docker.com/get-docker/).

=== "Linux"

    ```bash
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    ```

    Then log out and back in.

=== "Mac"

    Requires [Homebrew](https://brew.sh/). After installing, open the Docker app once to start it.

    ```bash
    brew install --cask docker
    ```

=== "Windows"

    Install Windows Subsystem for Linux (WSL2), In PowerShell as Administrator, run:
    `wsl --install`

    Reboot your computer, then download the [Docker Desktop installer](https://www.docker.com/get-started/). If you don't know whether you have AMD64 or ARM64 architecture, you can check by opening a PowerShell window and running the command `systeminfo | findstr /B /C:"System Type"`. If it says "x64-based PC", you have AMD64 architecture. If it says "ARM-based PC", you have ARM64 architecture.
    
    Run the installer, using the recommended settings (specifically, installing for the user only).


### Optional: Download all OFO Docker images in advance

Each OFO tutorial task includes code that will download the Docker image(s) required for that task. However, downloads can be slow depending on your internet connection. If you want to download all OFO Docker images in advance so you don't have to wait for downloads when going through the tutorials, you can run the following commands.

```bash
docker pull ghcr.io/open-forest-observatory/tree-detection-framework
docker pull ghcr.io/open-forest-observatory/tree-classification-framework
docker pull ghcr.io/open-forest-observatory/tree-registration-and-matching
docker pull ghcr.io/open-forest-observatory/geograypher
docker pull ghcr.io/open-forest-observatory/mmpretrain
```

These commands work the same on Linux, Mac, and Windows (PowerShell). The images are several gigabytes each, so make sure you have sufficient disk space.

## Native Python

OFO tools are written in Python, so they can also be run directly on your computer without using Docker. This requires installing Python and the required Python libraries and other system dependencies. This process involves a few more steps than Docker, but a big benefit is that you can then run the OFO tools directly in a Python environment, such as a Jupyter notebook (see below). This allows you to integrate OFO data processing with other Python code--for example, code to prepare the input data and visualize the output data. Each OFO tutorial task includes instructions for installing the required Python libraries and other dependencies and for running the OFO tools directly in Python.

When running OFO tools as Python code directly, you will first need to load the required libraries into memory. Each OFO tutorial includes code demonstrating how to do this. After loading the libraries, you can run the OFO tools directly in Python.

There are three common ways to run Python code: in a Jupyter notebook, as a standalone script, or as a command-line entrypoint (all described below).

Regardless how you will run Python code, you will need to have the required Python libraries and other dependencies installed in your Python environment. Installing Python libraries and their dependencies on a computer requires creating a Python *environment*, which is a self-contained installation of Python and the relevant libraries. The OFO recommends the [Conda](https://docs.conda.io/en/latest/) system for creating and managing Python environments. Each OFO tutorial task includes instructions for creating a Conda environment and installing the required Python libraries and other dependencies in that environment. To be able to do this, you need to have Conda and Poetry installed on your computer.


### Install Conda

We recommend installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html) because it is smaller and simpler than the full Anaconda distribution and contains everything you need.

=== "Linux"

    ```bash
    curl -fsSLO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -m).sh
    bash Miniconda3-latest-Linux-$(uname -m).sh
    ```

    Follow the prompts, then close and reopen your terminal.

=== "Mac"

    ```bash
    brew install --cask miniconda
    conda init "$(basename "$SHELL")"
    ```

    Then close and reopen your terminal.

=== "Windows"

    In PowerShell:

    ```powershell
    winget install Anaconda.Miniconda3
    ```

    Then open "Anaconda Prompt" from the Start menu and run the following once to make `conda` available in PowerShell:

    ```powershell
    conda init powershell
    ```

    Close and reopen PowerShell. If you see an error about running scripts being disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` and reopen PowerShell again.

    You should now be able to access Conda from PowerShell and Anaconda Prompt.

Confirm it works by running `conda --version` in a terminal.

### Install Poetry

[Poetry](https://python-poetry.org/) is a tool for installing Python libraries. Many OFO tools list their required libraries (and the exact versions to use) in a file called `pyproject.toml`, and Poetry reads that file to install everything the tool needs into your active Conda environment. Follow the [Poetry installation instructions](https://python-poetry.org/docs/#installation) to install it, then confirm it works by running `poetry --version` in a terminal.


### Python command-line entrypoints

The OFO provides command-line entrypoints for each of its tools. These are Python code files that can be run from a terminal window with a single command. Inside, they load the required Python libraries and call the relevant Python functions to perform the task. They provide standardized handling of processing parameters that are provided by the user in the command line call. The command-line entrypoints are useful for users who are not familiar with Python, as they can simply be run as provided and do not require any modifications to the Python code. Each OFO tutorial task includes instructions for running the command-line entrypoints for that task. Here is an example of running a command-line entrypoint to detect trees from a canopy height model using the OFO [Tree Detection Framework](https://github.com/open-forest-observatory/tree-detection-framework):

```bash
conda activate tree-detection-framework
python -m tree_detection_framework.entrypoints.detect_geometric_two_stage \
    path/to/data/drone/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
    path/to/data/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
    --raster-blur-sigma 0.5 \
```

### Jupyter notebooks

One way to run Python code is in a [Jupyter notebook](https://jupyter.org/), which is an interactive document that can contain both text and code that can be run. Jupyter notebooks are useful for data processing tasks because they allow you to run code in small chunks and see the results immediately, which is helpful for exploring data and debugging code. Each OFO tutorial task includes a Jupyter notebook that performs each step. Jupyter notebooks run inside a Conda environment; they are not an alternative to Conda.

TODO: Instructions on how to install Jupyter (link to Jupyter documentation), access the Jupyter server, and run notebooks, including connecting to the right Python environment.

### Custom Python scripts

Python code can also be run as standalone scripts, outside of Jupyter notebooks. Scripts are simply files containing Python code that can be run from a terminal window or inside an IDE such as [VS Code](https://code.visualstudio.com/) or [Positron](https://positron.posit.co/). Each OFO tutorial provides the Python code snippets to accomplish each step, but it is the user's responsibility to piece them together into a complete script. From a terminal, you would run a script like this:

```bash
conda activate my-environment # Activate the Conda environment containing the required libraries
python path/to/my-script.py   # Run the script
```

### Setting up all Python environments in advance

Each OFO tutorial task includes instructions to set up the Python environment required for tools used by that task. However, setup can be slow, especially on slow to moderate speed internet connections, due to library downloads. If you want to set up all Python environments in advance so you don't have to wait for downloads when going through the tutorials, run the installation instructions associated with each tool in the [Glossary of tools](glossary-of-tools.md).
