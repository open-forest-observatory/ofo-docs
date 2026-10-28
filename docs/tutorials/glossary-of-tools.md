---
weight: 101
# To make a tool linkable from any page by writing it in square brackets, add
# it (and any variants, e.g. plurals) to includes/glossary-links.md, pointing
# to its heading anchor.
---

# Glossary of tools

This page describes the key software tools used in the OFO tutorials.

## OFO tools

### Tree Detection Framework (TDF) { #tdf }

A Python library for detecting and delineating individual trees from drone-derived data products. It provides a geometric algorithm that finds treetops in a [canopy height model] and a common interface to several existing computer vision models that detect trees in an [orthomosaic]. It eliminates the need for common 'boilerplate' pre- and post-processing code, including dividing large geospatial rasters into the smaller tiles expected by computer vision models and reassbmeling the results. It facilitates comparing among different computer vision models, using consistent inputs and outputs. [Documentation](https://open-forest-observatory.github.io/tree-detection-framework/)

??? info "Installation instructions"

    **Docker or local Python?** The instructions below describe how to install TDF in a local Python environment. Alternatively, you can use the [Docker] image `ghcr.io/open-forest-observatory/tree-detection-framework` and access the library's [entrypoints](https://open-forest-observatory.github.io/tree-detection-framework/command_line_usage/).

    This installs TDF into a [Conda] environment. You will need Conda and Poetry installed first (see [Preparation](preparation.md)). See the [TDF installation documentation](https://open-forest-observatory.github.io/tree-detection-framework/getting_started/installation/) for full installation details. Here we provide quick install instructions including support for Detectree2 and SAM2.

    === "Linux / Mac"

        ```bash
        # Core components
        git clone https://github.com/open-forest-observatory/tree-detection-framework.git
        cd tree-detection-framework
        conda create -n tree-detection-framework python=3.10 -y
        conda activate tree-detection-framework
        poetry install

        # Detectree2 support
        pip install --no-build-isolation git+https://github.com/facebookresearch/detectron2.git
        mkdir -p checkpoints/detectree2
        curl -L -o checkpoints/detectree2/230103_randresize_full.pth https://zenodo.org/records/10522461/files/230103_randresize_full.pth

        # SAM2 support
        cd ..
        git clone https://github.com/facebookresearch/sam2.git
        cd sam2
        pip install -e .
        cd checkpoints && ./download_ckpts.sh && cd ..
        mv checkpoints/* ../tree-detection-framework/checkpoints/
        cd ../tree-detection-framework
        ```

    === "Windows"

        Run these in Anaconda Prompt or PowerShell. The SAM2 checkpoints are downloaded directly because the SAM2 download script is a Linux/Mac shell script.

        ```powershell
        # Core components
        git clone https://github.com/open-forest-observatory/tree-detection-framework.git
        cd tree-detection-framework
        conda create -n tree-detection-framework python=3.10 -y
        conda activate tree-detection-framework
        poetry install

        # Detectree2 support
        pip install --no-build-isolation git+https://github.com/facebookresearch/detectron2.git
        mkdir checkpoints\detectree2
        curl.exe -L -o checkpoints\detectree2\230103_randresize_full.pth https://zenodo.org/records/10522461/files/230103_randresize_full.pth

        # SAM2 support
        cd ..
        git clone https://github.com/facebookresearch/sam2.git
        cd sam2
        pip install -e .
        cd ..\tree-detection-framework\checkpoints
        $base = "https://dl.fbaipublicfiles.com/segment_anything_2/092824"
        foreach ($m in "tiny", "small", "base_plus", "large") {
            curl.exe -L -O "$base/sam2.1_hiera_$m.pt"
        }
        cd ..
        ```

### Geograypher { #geograypher }

A Python library that translates between pixel coordinates in raw drone images (x,y) and geospatial coordinates (lon, lat) -- and vice versa -- using the photogrammetry-derived camera positions and a 3D [mesh model] of the site. In the tutorials, it is used to render the unique ID of each detected tree into the view of every drone photo in which that tree appears. [Documentation](https://open-forest-observatory.github.io/geograypher/)

??? info "Installation instructions"

    **Docker or local Python?** The instructions below describe how to install Geograypher in a local Python environment. Alternatively, you can use the [Docker] image `ghcr.io/open-forest-observatory/geograypher` to access the library's [entrypoints](https://open-forest-observatory.github.io/geograypher/API_reference/entrypoints/).

    This installs Geograypher into a [Conda] environment. You will need Conda installed first (see [Preparation](preparation.md)).

    ```bash
    conda create -n geograypher -c conda-forge python=3.9 -y
    conda activate geograypher
    pip install geograypher
    ```

    Rendering 3D views on a headless Linux machine (such as a remote server with no display) requires a virtual frame buffer, which can be installed with `sudo apt install xvfb`.

    See the [Geograypher installation documentation](https://open-forest-observatory.github.io/geograypher/getting_started/installation/) for full installation details, including the developer install (which uses Poetry) if you plan to modify Geograypher's code.

### Tree Classification Framework (TCF) { #tcf }

A Python library for predicting tree attributes, such as species and live/dead status, from raw drone photos. In the tutorials it crops each view of each detected tree out of the drone photos, preparing the crops for a computer vision classification model, and afterward aggregates the predictions for all crops of a tree into a single prediction for that tree. [Source code](https://github.com/open-forest-observatory/tree-classification-framework)

??? info "Installation instructions"

    **Docker or local Python?** The instructions below describe how to install TCF in a local Python environment. Alternatively, you can use the [Docker] image `ghcr.io/open-forest-observatory/tree-classification-framework` to access the library's [entrypoints](https://github.com/open-forest-observatory/tree-classification-framework#scripts).

    This installs TCF into a [Conda] environment. You will need Conda and Poetry installed first (see [Preparation](preparation.md)).

    ```bash
    git clone https://github.com/open-forest-observatory/tree-classification-framework.git
    cd tree-classification-framework
    conda create -n tree-classification-framework python=3.12 -y
    conda activate tree-classification-framework
    poetry install
    ```

    TCF prepares the inputs for, and aggregates the outputs of, a classification model, but it does not run the model itself. In the tutorials the model is run with the OFO fork of [MMPretrain], installed in a separate Conda environment. TCF also relies on [Geograypher] for rendering, which likewise has its own environment.

    See the full [TCF installation instructions](https://github.com/open-forest-observatory/tree-classification-framework#install) for more details.

### Tree Registration and Matching Toolkit (TRAM) { #tram }

A Python library for spatially aligning and comparing different tree maps. It can estimate the spatial offset between a ground reference (manual inventory) tree map and drone-derived data, such as a [canopy height model] or set of detected trees. It also matches the corresponding trees between two datasets (e.g., ground survey and drone detections), allowing a spatial tolerance. Finally, it supports computing metrics of agreement (detection accuracy), such as recall and precision, between two tree maps. [Source code](https://github.com/open-forest-observatory/tree-registration-and-matching)

??? info "Installation instructions"

    **Docker or local Python?** The instructions below describe how to install TRAM in a local Python environment. Alternatively, you can use the [Docker] image `ghcr.io/open-forest-observatory/tree-registration-and-matching` to access the library's [entrypoints](https://github.com/open-forest-observatory/tree-registration-and-matching/tree/main/tree_registration_and_matching/entrypoints).

    This installs TRAM into a [Conda] environment. You will need Conda and Poetry installed first (see [Preparation](preparation.md)).

    ```bash
    git clone https://github.com/open-forest-observatory/tree-registration-and-matching.git
    cd tree-registration-and-matching
    conda create -n tree-registration-and-matching python=3.12 -y
    conda activate tree-registration-and-matching
    poetry install
    ```

    See the [TRAM installation instructions](https://github.com/open-forest-observatory/tree-registration-and-matching/tree/main#install) for more details.


## External tools

### DeepForest { #deepforest }

A computer vision model, pretrained on airborne imagery, that predicts a rectangular bounding box around each tree crown in an [orthomosaic]. In the tutorials it is run via the [Tree Detection Framework]. [Project page](https://deepforest.readthedocs.io/)

### Detectree2 { #detectree2 }

A computer vision model, based on Mask R-CNN, that delineates individual tree crowns as polygons in an [orthomosaic]. In the tutorials it is run via the [Tree Detection Framework]. [Documentation](https://patball1.github.io/detectree2/)

### SAM2 { #sam2 }

Segment Anything Model 2, an external general-purpose image segmentation model from Meta that produces object masks from prompts such as points or boxes (or no prompts). In the tutorials it is run via the [Tree Detection Framework] to delineate tree crowns in an [orthomosaic]. [Project page](https://ai.meta.com/sam2)

### SAM3 { #sam3 }

Segment Anything Model 3, the successor to [SAM2] from Meta, which can detect and segment objects in images from text prompts or example images as well as points and boxes. It can be run via the [Tree Detection Framework] to delineate tree crowns in an [orthomosaic]. [Project page](https://ai.meta.com/sam3/)

### MMPretrain { #mmpretrain }

An external toolbox that simplifies training and running computer vision image classification models. In the tutorials, the OFO fork (a modified copy) of MMPretrain applies previously trained models to the cropped tree images to predict each tree's species and live/dead status. [Documentation](https://mmpretrain.readthedocs.io/), [OFO fork](https://github.com/open-forest-observatory/mmpretrain)

??? info "Installation instructions"

    It is very difficult to install the dependencies for MMPretrain, and the exact steps depend on your system. Therefore, it is strongly recommended that you run MMPretrain using [Docker] rather than a local Python environment. You can use the Docker image `ghcr.io/open-forest-observatory/mmpretrain` to run the OFO fork's [prediction tool](https://github.com/open-forest-observatory/mmpretrain/tree/main/tools) (`tools/predict.py`). See the [classification tutorial](itd/2_classification.md) for an example command.

    If you must install locally, follow the [OFO fork installation instructions](https://github.com/open-forest-observatory/mmpretrain#installation) to create a separate [Conda] environment, as MMPretrain's dependencies are likely to conflict with those of other OFO tools.

### Docker { #docker }

A system for distributing software together with all of its dependencies in a container that runs the same way on any operating system. OFO provides a Docker _image_ (the blueprint for a container) for each of its tools, so the tutorials can be run without installing Python libraries directly. See the [Docker guide](/tutorials/preparation.md#docker) for installation and usage. [Docker website](https://www.docker.com/)

### Conda { #conda }

A package and environment manager that installs Python libraries and their non-Python dependencies into isolated environments. It is used to run OFO tools directly in Python, without Docker, by keeping each tool's dependencies separate from the others. We recommend the minimal [Miniconda](https://docs.conda.io/en/latest/miniconda.html) distribution.

### Jupyter { #jupyter }

A system for creating interactive notebooks that combine text, code, and the results of running the code. Notebooks are one of the ways to run OFO Python code step by step and inspect intermediate results. [Project page](https://jupyter.org/)

### QGIS { #qgis }

A free, open-source geographic information system (GIS) application for viewing, editing, and analyzing geospatial data. In the tutorials it is used to visualize outputs such as detected tree points and crown polygons over rasters like the [canopy height model] and [orthomosaic]. [Project page](https://qgis.org/)
