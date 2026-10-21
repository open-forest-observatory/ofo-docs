---
weight: 30
---

# Task 2: Classification

We will use the OFO tools [Geograypher](https://github.com/open-forest-observatory/tree-detection-framework) and [Tree Classification Framework](https://github.com/open-forest-observatory/tree-classification-framework) and an OFO fork of [MMPretrain](https://github.com/open-forest-observatory/mmpretrain) to generate predictions of tree species and live/dead status for detected trees. We will use all of the views of each detected tree from each drone photo it appears in. Because the raw drone photos are not geospatial data products, some intermediate processing using OFO tools is required.The process follows this workflow:

 - Use Geograypher to render the unique ID of each detected tree to the perspective of each image it appears in
 - Use the Tree Classification Framework to crop out each view of each tree from each drone photo it appears, while preserving the unique ID of the tree
 - Use the OFO fork of MMPretrain to generate a prediction of species and live/dead status for each individual tree crop
 - Use the Tree Classification Framework to aggregate the predictions for each individual tree crop into a single geospatial prediction for each detected tree.

## Required input data

| Name                            | Source         | Example file                                                                                            |
| ------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------- |
| Raw drone photos                | Drone flight   | [drone/raw-drone-photos/composite1](https://ucdavis.box.com/s/p2w2cw4bjrsjwjgcr11m1luqh89v3fxh)               |
| Photogrammetry camera locations | Photogrammetry | [composite1_cameras.xml](https://ucdavis.box.com/s/qallapylahuq7u76dv9fef8tp2aoxlyp)                    |
| Photogrammetry [mesh] | Photogrammetry | [composite1_mesh.ply](https://ucdavis.box.com/s/lgulbgesty4i95bep12c94v2rhxb1a8p)                    |
| [Digital terrain model] | Photogrammetry | [composite1_dtm-ptcloud.tif](https://ucdavis.box.com/s/s3jmpxs90d3qlk92k8n8odjrxboyfows)                    |
| Detected tree crowns            | Tree detection | [composite1_tree-crowns_geometric_v01.gpkg](https://ucdavis.box.com/s/ormrucvnmrgj0qhpt0hs63mij8kjs9q6) |
| Species and live/dead classification models            | Model training (beyond tutorial scope) | [cv-models](https://ucdavis.box.com/s/sx6p6cgzhzafl33x6eigh6v5lvy4x8z6) |

The detected tree crowns may be ones you produced in the [Detection task](/tutorials/itd/1_detection.md), or you can use the pre-generated detections in the tutorial data folder (linked above). It is important that the detections and photogrammetry camera locations be derived from the same photogrammetry run, using the same raw drone photos that you will use for this task.

## Setup

!!! info "Before you begin"

    Make sure you have gone through the [OFO tutorial preparation](/tutorials/index.md#preparing-to-follow-the-tutorials) guidance.
=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/index.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

=== "Python command-line entrypoint"

    This workflow requires three separate environments, for each `geograypher`, `tree-classification-framework`, and `mmpretrain`.

    Install `geograypher` following its [installation instructions](https://open-forest-observatory.github.io/geograypher/getting_started/installation/#advanceddeveloper-installation).

    Install `tree-classification-framework` following its [installation instructions](https://github.com/open-forest-observatory/tree-classification-framework#install).

    Install `MMPretrain` following its [installation instructions](https://github.com/open-forest-observatory/mmpretrain#installation).
    - TODO this fails with the following error `ImportError: /home/exouser/miniconda3/envs/open-mmlab/lib/python3.8/site-packages/torch/lib/libtorch_cpu.so: undefined symbol: iJIT_NotifyEvent`.


=== "Custom Python script"
    TODO same as above


## Rendering tree locations to images

The first step in classifying trees is use `Geograypher` to understand what region of each image observes each tree. The first two inputs are from photogrammetry: the 3D structure of the scene represented as a [mesh] and the location and orientation from which each image was captured. The 2D geospatial locations of the tree crowns is also obtained using the detection algorithm in the last section. Additionally, the digital terrain model ([DTM]) from photogrammetry is used in this particular application for determining which part of the mesh represent the ground.

Each tree is assigned a unique numerical ID when it is detected. Since the mesh has geospatial reference information, these IDs can be transfered from the 2D representation of the crowns to the corresponding 3D mesh faces. From there, techniques from computer graphics are used to render the IDs from the mesh to the perspective of each image. Norably, this rendering process is oclusion-aware, so if a tree is blocked from view by another obstacle, it will not be spuriously rendered. This produces a single-channel image encoding the ID of the observed tree (or a special background ID) at each pixel, for each image in the original set of drone images.

The original drone images are not required at this stage except for visualization. An example is shown below of the rendered individual tree IDs rendered to the perspective of the image, and overlaid on it.

![rendered-IDs](/assets/images/tutorials/composite1_rendered-ids.png)

=== "Docker (recommended)"

    ```bash
    export DATA_DIR="path/to/data/"

    docker run --rm --user "$(id -u):$(id -g)" \
    -v "${DATA_DIR}:/data" \
    ghcr.io/open-forest-observatory/geograypher:latest \
    python -m geograypher.entrypoints.render_labels \
        --mesh-file /data/drone/photogrammetry-outputs/composite1_mesh.ply \
        --mesh-CRS 32610 \
        --cameras-file  /data/drone/photogrammetry-outputs/composite1_cameras.xml \
        --texture /data/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
        --texture-column-name unique_ID \
        --image-folder /data/drone/raw-drone-photos/composite1 \
        --render-savefolder /data/renders \
        --original-image-folder /data/drone/raw-drone-photos \
        --labels-vis-folder /data/renders-vis \
        --mesh-ROI-buffer-radius-meters 10 \
        --cameras-ROI-buffer-radius-meters 20 \
        --render-image-scale 0.125 \
        --DTM-file /data/drone/photogrammetry-postprocessed/full/composite1_dtm-ptcloud.tif \
        --ground-height-threshold 2.0
    ```

=== "Python command-line entrypoint"

    ```bash
    export DATA_FOLDER="path/to/data/"

    conda activate geograypher

    python -m geograypher.entrypoints.render_labels \
        --mesh-file ${DATA_FOLDER}/drone/photogrammetry-outputs/composite1_mesh.ply \
        --mesh-CRS 32610 \
        --cameras-file  ${DATA_FOLDER}/drone/photogrammetry-outputs/composite1_cameras.xml \
        --texture ${DATA_FOLDER}/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
        --texture-column-name unique_ID \
        --image-folder ${DATA_FOLDER}/drone/raw-drone-photos/composite1 \
        --render-savefolder ${DATA_FOLDER}/renders \
        --original-image-folder ${DATA_FOLDER}/drone/raw-drone-photos \
        --labels-vis-folder ${DATA_FOLDER}/renders-vis \
        --mesh-ROI-buffer-radius-meters 10 \
        --cameras-ROI-buffer-radius-meters 20 \
        --render-image-scale 0.125 \
        --DTM-file ${DATA_FOLDER}/drone/photogrammetry-postprocessed/full/composite1_dtm-ptcloud.tif \
        --ground-height-threshold 2.0
    ```

=== "Custom Python script"

    ```bash
    conda activate geograypher
    ```

    # TODO Then load the required libraries:

    ```python
    # TODO: Complete python lines to load libraries
    ```


## Crop the view of each tree from each drone photo

The last step identifies the location of each tree in each image, but additional processing is required to prepare this data for a computer vision predition model. Specifically, we use a classification model which takes an image and produces a single label. To accomdate this format, we must create one image per view of each tree. Using the rendered mask from geograypher, a rectangular region surrounding each observed tree is cropped from the original image. Then, any content within the crop but outside the bounds of the tree is set to a background color. Finally, each chip is written out, while preserving both the structure of what image it was derived from and the ID of the tree it was generated from.

![crop](/assets/images/tutorials/composite1_crop.png)

TODO: Illustrative schematic here?

=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/index.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

    ```bash
    export DATA_FOLDER="path/to/data/"

    conda activate tree-classification-framework

    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_FOLDER}:/data" \
        ghcr.io/open-forest-observatory/tree-classification-framework:latest \
        python -m tree_classification_framework.chip_images \
           /data/drone/raw-drone-photos/composite1 \
           /data/renders \
           /data/drone/tree-chips \
           --n-workers 4 \
           --n-chips-per-tree 10
    ```

=== "Python command-line entrypoint"

    ```bash
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"

    python -m tree_classification_framework.chip_images \
       ${DATA_FOLDER}/drone/raw-drone-photos/composite1 \
       ${DATA_FOLDER}/renders \
       ${DATA_FOLDER}/drone/tree-chips \
       --n-workers 4 \
       --n-chips-per-tree 10
    ```

=== "Custom Python script"

    TODO:

## Classify each crop

We can use models previously trained by the OFO to classify each chip. In this step, we'll use two independent models: one for predicting live vs. dead trees and another for prediction species. The latter model is illustrative and was developed for eight common species in western mixed conifer forests. These models are used to classify each chip independently, and one file is created for each of the species and live/dead prediction results, summarizing the predicted class for each image.

TODO: Illustrative schematic here? This one is probably the most conceptually simple.

=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/index.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

    ```bash
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"

    docker run --rm --user "$(id -u):$(id -g)" \
        --gpus all --group-add "$(stat -c %g /dev/nvidia0)" \
        -v "${DATA_FOLDER}:/data" \
        ghcr.io/open-forest-observatory/mmpretrain:latest \
        python /app/tools/predict.py \
           /data/drone/tree-chips \
           /data/cv-models/dead_live_config.py \
           /data/cv-models/dead_live_model.pth \
           /data/per-chip-classifications/classified-live-dead.json
    ```
    Note that you can run the species prediction step by replacing `live_dead` with `species` in all lines.

=== "Python command-line entrypoint"

    It is very difficult to install the dependencies for `MMPretrain` and the exact steps depend on
    your system. Therefore, it is strongly recommended that you use the docker version to run this
    step.

=== "Custom Python script"

    It is very difficult to install the dependencies for `MMPretrain` and the exact steps depend on
    your system. Therefore, it is strongly recommended that you use the docker version to run this
    step.

## Assign predictions to individual trees

The end goal of this process is to have geospatial, tree-level predictions. Each tree is likely to been observed many times from different viewpoints and will therefore have multiple classification results. We maintain the tree's unique ID through all steps in the process, so the view-level predictions still tie back to a specific tree. Since predictions may differ across views, we take the modal (most common) prediction across all views, and assign this as the predicted tree label. This information is joined with the geospatial crown information that was orignally used to generate the chips and saved out. In addition to the predicted class, we also include the number of views which contributed to the prediction and the fraction of views that agreed with the modal prediction. These attributes are suffixed with `_n_preds` and `_frac_matching_mode`, respectively, and may be used in downstream tasks to filter out low-confidence predictions.

TODO: Illustrative schematic here?

=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/index.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

    ```bash
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"

    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_FOLDER}:/data" \
        ghcr.io/open-forest-observatory/tree-classification-framework:latest \
        python -m tree_classification_framework.assign_predictions_to_trees \
           /data/per-chip-classifications/classified-live-dead.json \
           live_dead \
           /data/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
           /data/classified-trees/composite1_tree-crowns_geometric_v01_live_dead.gpkg
    ```
    Note that you can run the species prediction step by replacing `live_dead` with `species` in all lines.

=== "Python command-line entrypoint"

    TODO: This can just be the TCF installation instructions I think

    ```bash
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"

    conda activate tree-classification-framework

    python -m tree_classification_framework.assign_predictions_to_trees \
       ${DATA_FOLDER}/per-chip-classifications/classified-species.json \
       species \
       ${DATA_FOLDER}/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
       ${DATA_FOLDER}/classified-trees/composite1_tree-crowns_geometric_v01_species.gpkg
    ```
    Note that you can run the species prediction step by replacing `live_dead` with `species` in all lines.

=== "Custom Python script"
    TODO:
