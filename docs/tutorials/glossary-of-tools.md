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

#### Installation

TODO: Installation text

### Geograypher { #geograypher }

A Python library that translates between pixel coordinates in raw drone images (x,y) and geospatial coordinates (lon, lat) -- and vice versa -- using the photogrammetry-derived camera positions and a 3D [mesh model] of the site. In the tutorials, it is used to render the unique ID of each detected tree into the view of every drone photo in which that tree appears. [Documentation](https://open-forest-observatory.github.io/geograypher/)

#### Installation instructions

TODO: installation text

### Tree Classification Framework (TCF) { #tcf }

A Python library for predicting tree attributes, such as species and live/dead status, from raw drone photos. In the tutorials it crops each view of each detected tree out of the drone photos, preparing the crops for a computer vision classification model, and afterward aggregates the predictions for all crops of a tree into a single prediction for that tree. [Source code](https://github.com/open-forest-observatory/tree-classification-framework)

#### Installation instructions

TODO: Installation text

### Tree Registration and Matching Toolkit (TRAM) { #tram }

A Python library for spatially aligning and comparing different tree maps. It can estimate the spatial offset between a ground reference (manual inventory) tree map and drone-derived data, such as a [canopy height model] or set of detected trees. It also matches the corresponding trees between two datasets (e.g., ground survey and drone detections), allowing a spatial tolerance. Finally, it supports computing metrics of agreement (detection accuracy), such as recall and precision, from . [Source code](https://github.com/open-forest-observatory/tree-registration-and-matching)

#### Installation instructions

TODO: Installation text


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

### Docker { #docker }

A system for distributing software together with all of its dependencies in a container that runs the same way on any operating system. OFO provides a Docker _image_ (the blueprint for a container) for each of its tools, so the tutorials can be run without installing Python libraries directly. See the [Docker guide](/tutorials/index.md#docker) for installation and usage. [Project page](https://www.docker.com/)

### Conda { #conda }

A package and environment manager that installs Python libraries and their non-Python dependencies into isolated environments. It is used to run OFO tools directly in Python, without Docker, by keeping each tool's dependencies separate from the others. We recommend the minimal [Miniconda](https://docs.conda.io/en/latest/miniconda.html) distribution.

### Jupyter { #jupyter }

A system for creating interactive notebooks that combine text, code, and the results of running the code. Notebooks are one of the ways to run OFO Python code step by step and inspect intermediate results. [Project page](https://jupyter.org/)

### QGIS { #qgis }

A free, open-source geographic information system (GIS) application for viewing, editing, and analyzing geospatial data. In the tutorials it is used to visualize outputs such as detected tree points and crown polygons over rasters like the [canopy height model] and [orthomosaic]. [Project page](https://qgis.org/)
