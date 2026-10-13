---
weight: 30
---

# Task 2: Classification

We will use the OFO tools [Geograypher](https://github.com/open-forest-observatory/tree-detection-framework) and [Tree Classification Framework](https://github.com/open-forest-observatory/tree-classification-framework) to generate predictions of tree species and live/dead status for detected trees. We will use all of the views of each detected tree from each drone photo it appears in. Because the raw drone photos are not geospatial data products, some intermediate processing using OFO tools is required.The process follows this workflow:

 - Use Geograypher to render the unique ID of each detected tree to the perspective of each image it appears in
 - Use the Tree Classification Framework to crop out each view of each tree from each drone photo it appears, while preserving the unique ID of the tree
 - Use the Tree Classification Framework to generate a prediction of species and live/dead status for each individual tree crop
 - Use the Tree Classification Framework to aggregate the predictions for each individual tree crop into a single prediction for each detected tree.

TODO: Consider moving the above text into the actual workflow sections below.

TODO: Consider adding illustrative schematics here or (more likely) below.


## Required input data

| Name                            | Source         | Example file                                                                                            |
| ------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------- |
| Raw drone photos                | Drone flight   | [raw-drone-photos/composite1](https://ucdavis.box.com/s/p2w2cw4bjrsjwjgcr11m1luqh89v3fxh)               |
| Photogrammetry camera locations | Photogrammetry | [composite1_cameras.xml](https://ucdavis.box.com/s/qallapylahuq7u76dv9fef8tp2aoxlyp)                    |
| Photogrammetry mesh | Photogrammetry | [composite1_mesh.ply](https://ucdavis.box.com/s/lgulbgesty4i95bep12c94v2rhxb1a8p)                    |
| Digital terrain model | Photogrammetry | [composite1_dtm-ptcloud.tif](https://ucdavis.box.com/s/s3jmpxs90d3qlk92k8n8odjrxboyfows)                    |
| Detected tree crowns            | Tree detection | [composite1_tree-crowns_geometric_v01.gpkg](https://ucdavis.box.com/s/ormrucvnmrgj0qhpt0hs63mij8kjs9q6) |

The detected tree crowns may be ones you produced in the [Detection task](/tutorials/itd/1_detection.md), or you can use the pre-generated detections in the tutorial data folder (linked above). It is important that the detections and photogrammetry camera locations be derived from the same photogrammetry run, using the same raw drone photos that you will use for this task.

## Setup

!!! info "Before you begin"

    Make sure you have gone through the [OFO tutorial preparation](/tutorials/index.md#preparing-to-follow-the-tutorials) guidance.

=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/index.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

    ```bash
    export DATA_DIR="/ofo-share/repos/david/ofo-docs/data"
    docker run --rm --user "$(id -u):$(id -g)" \
    -v "${DATA_DIR}:/data" \
    ghcr.io/open-forest-observatory/geograypher:latest \
    python -m geograypher.entrypoints.render_labels \
        --mesh-file /data/inputs/drone/photogrammetry-outputs/composite1_mesh.ply \
        --mesh-CRS 32610 \
        --cameras-file  /data/inputs/drone/photogrammetry-outputs/composite1_cameras.xml \
        --texture /data/outputs/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
        --texture-column-name unique_ID \
        --image-folder /data/inputs/drone/raw-drone-photos/composite1 \
        --render-savefolder /data/intermediate/renders \
        --original-image-folder /data/raw-drone-photos \
        --labels-vis-folder /data/intermediate/renders-vis \
        --mesh-ROI-buffer-radius-meters 10 \
        --cameras-ROI-buffer-radius-meters 20 \
        --render-image-scale 0.125 \
        --DTM-file /data/inputs/drone/photogrammetry-postprocessed/full/composite1_dtm-ptcloud.tif \
        --ground-height-threshold 2.0
    ```

=== "Python command-line entrypoint"

    TODO: Need to merge the install instructions for both tools here?

    Install the Geograypher and Tree Classification Framework libraries and their dependencies into a Conda environment following their [installation instructions](https://open-forest-observatory.github.io/tree-detection-framework/getting_started/installation/), then activate the Conda environment in a terminal window:

    ```bash
    conda activate TODO: Name of the Conda environment
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"
    python -m geograypher.entrypoints.render_labels \
        --mesh-file ${DATA_FOLDER}/inputs/drone/photogrammetry-outputs/composite1_mesh.ply \
        --mesh-CRS 32610 \
        --cameras-file  ${DATA_FOLDER}/inputs/drone/photogrammetry-outputs/composite1_cameras.xml \
        --texture ${DATA_FOLDER}/outputs/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
        --texture-column-name unique_ID \
        --image-folder ${DATA_FOLDER}/inputs/drone/raw-drone-photos/composite1 \
        --render-savefolder ${DATA_FOLDER}/intermediate/renders \
        --original-image-folder /data/raw-drone-photos \
        --labels-vis-folder ${DATA_FOLDER}/intermediate/renders-vis \
        --mesh-ROI-buffer-radius-meters 10 \
        --cameras-ROI-buffer-radius-meters 20 \
        --render-image-scale 0.125 \
        --DTM-file ${DATA_FOLDER}/inputs/drone/photogrammetry-postprocessed/full/composite1_dtm-ptcloud.tif \
        --ground-height-threshold 2.0
    ```

=== "Custom Python script"

    TODO: Repeat the Conda env instructions from above once complete.

     Then load the required libraries:

    ```python
    # TODO: Complete python lines to load libraries
    ```


## Crop the view of each tree from each drone photo

Before we can use computer vision to classify trees to species, we need to:

- Take the geospatial tree crowns that we detected in the [Detection task](/tutorials/itd/1_detection.md)
- For detected tree crown, find all the drone photos it appeared in
- For each photo the tree appeared in crop the view of it from the photo.

This means that ultimately, for every geospatial tree crown, we will end up with multiple cropped images, each from a different viewpoint.

TODO: Illustrative schematic here?