---
weight: 30
---

# Task 2: Classification

Our goal here is to predict the species and live/dead status of every detected tree using computer vision applied to the _raw drone photos_. To do this, we will use the OFO tools [Geograypher](https://github.com/open-forest-observatory/tree-detection-framework) and [Tree Classification Framework](https://github.com/open-forest-observatory/tree-classification-framework) and an OFO fork (modification) of [MMPretrain](https://github.com/open-forest-observatory/mmpretrain), an external tool that simplifies running computer vision models.

We will use all of the views of each detected tree from each drone photo it appears in. Because the raw drone photos are not geospatial data products, some intermediate processing using OFO tools is required. The process follows this workflow:

 - Use Geograypher to render the unique ID of each detected tree to the perspective of each image it appears in
 - Use the Tree Classification Framework to crop out each view of each tree from each drone photo it appears in, while preserving the unique ID of the tree
 - Use the OFO fork of MMPretrain to generate a prediction of species and live/dead status for each individual tree crop
 - Use the Tree Classification Framework to aggregate the predictions for each individual tree crop into a single geospatial prediction for each detected tree.

To translate between geospatial coordinates (detected trees) and raw drone photos, we will need 3D models of the site derived from processing the raw photos using photogrammetry.

## Required input data

| Name                            | Source         | Example file                                                                                            |
| ------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------- |
| Raw drone photos                | Drone flight   | [drone/raw-drone-photos/composite1](https://ucdavis.box.com/s/p2w2cw4bjrsjwjgcr11m1luqh89v3fxh)               |
| Photogrammetry camera locations | Photogrammetry | [composite1_cameras.xml](https://ucdavis.box.com/s/qallapylahuq7u76dv9fef8tp2aoxlyp)                    |
| Photogrammetry [mesh model] | Photogrammetry | [composite1_mesh.ply](https://ucdavis.box.com/s/lgulbgesty4i95bep12c94v2rhxb1a8p)                    |
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

    Install the same three environments as described for the Python command-line entrypoint. Each step below is run from a Python script in the corresponding environment (`geograypher`, `tree-classification-framework`, or `mmpretrain`).


## Rendering tree locations to images

The first step in classifying trees is use `Geograypher` to understand what region of each image observes each tree--or at a lower level, where in 3D geographic space is a given pixel from a raw drone image. The first two inputs are from photogrammetry: (a) the 3D structure of the scene represented as a [mesh model], and (b) the location and orientation from which each image was captured, produced by photogrammetry as an XML file. Additionally, the digital terrain model ([DTM]) (derived from post-processing photogrammetry products) is used in this particular application for determining which part of the mesh represent the ground. Finally, we require the 2D geospatial locations of the detected tree crowns, obtained using a detection algorithm such as those demonstrated in [Task 1](/tutorials/itd/1_detection.md).

Fortunately, if we know the precise location of the camera sensor at at the time each image is captured (which we obtain from photogrammetry), along with the parameters of the camera's lens (also from photogrammetry), then we can use geometry to translate each pixel in a raw drone image into a _ray_ in 3D space. The place where this ray intersects the 3D mesh model is the location in 3D space that is represented by that pixel. Geograypher uses techniques from computer graphics to perform these calculations efficiently. Notably, this rendering process is occlusion-aware, so if one tree is in front of another from the camera's perspective, the pixel will be assigned to the tree in front.

![Image to mesh projection](/assets/images/tutorials/image-mesh-projection.png){ width="40%" }

Each tree is assigned a unique numerical ID when it is detected. Since the mesh model has geospatial reference information, these IDs can be transferred from the 2D geospatil representation of the crowns to the corresponding 3D mesh faces. Then, we use Geograypher to assign those IDs to the corresponding pixels in each raw drone image. This produces a single-channel image encoding the ID of the observed tree (or a special `background` ID) at each pixel, for each image in the original set of drone images.

The original drone images are not required at this stage except for visualization.

=== "Docker (recommended)"

    Linux/Mac:

    ```bash
    export DATA_DIR="path/to/data"

    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_DIR}:/data" \
        ghcr.io/open-forest-observatory/geograypher:latest \
        python -m geograypher.entrypoints.render_labels \
        --mesh-file /data/drone/photogrammetry-outputs/composite1_mesh.ply \
        --mesh-CRS 32610 \
        --cameras-file /data/drone/photogrammetry-outputs/composite1_cameras.xml \
        --texture /data/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
        --texture-column-name unique_ID \
        --image-folder /data/drone/raw-drone-photos/composite1 \
        --render-savefolder /data/renders \
        --original-image-folder /data/raw-drone-photos \
        --labels-vis-folder /data/renders-vis \
        --mesh-ROI-buffer-radius-meters 10 \
        --cameras-ROI-buffer-radius-meters 20 \
        --render-image-scale 0.125 \
        --DTM-file /data/drone/photogrammetry-postprocessed/full/composite1_dtm-ptcloud.tif \
        --ground-height-threshold 2.0
    ```

    Windows:

    ```powershell
    $env:DATA_DIR = "path\to\data"

    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/geograypher:latest `
        python -m geograypher.entrypoints.render_labels `
            --mesh-file /data/drone/photogrammetry-outputs/composite1_mesh.ply `
            --mesh-CRS 32610 `
            --cameras-file /data/drone/photogrammetry-outputs/composite1_cameras.xml `
            --texture /data/detected-trees/composite1_tree-crowns_geometric_v01.gpkg `
            --texture-column-name unique_ID `
            --image-folder /data/drone/raw-drone-photos/composite1 `
            --render-savefolder /data/renders `
            --original-image-folder /data/raw-drone-photos `
            --labels-vis-folder /data/renders-vis `
            --mesh-ROI-buffer-radius-meters 10 `
            --cameras-ROI-buffer-radius-meters 20 `
            --render-image-scale 0.125 `
            --DTM-file /data/drone/photogrammetry-postprocessed/full/composite1_dtm-ptcloud.tif `
            --ground-height-threshold 2.0
    ```

=== "Python command-line entrypoint"

    ```bash
    export DATA_DIR="path/to/data"

    conda activate geograypher

    python -m geograypher.entrypoints.render_labels \
        --mesh-file ${DATA_DIR}/drone/photogrammetry-outputs/composite1_mesh.ply \
        --mesh-CRS 32610 \
        --cameras-file ${DATA_DIR}/drone/photogrammetry-outputs/composite1_cameras.xml \
        --texture ${DATA_DIR}/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
        --texture-column-name unique_ID \
        --image-folder ${DATA_DIR}/drone/raw-drone-photos/composite1 \
        --render-savefolder ${DATA_DIR}/renders \
        --original-image-folder /data/raw-drone-photos \
        --labels-vis-folder ${DATA_DIR}/renders-vis \
        --mesh-ROI-buffer-radius-meters 10 \
        --cameras-ROI-buffer-radius-meters 20 \
        --render-image-scale 0.125 \
        --DTM-file ${DATA_DIR}/drone/photogrammetry-postprocessed/full/composite1_dtm-ptcloud.tif \
        --ground-height-threshold 2.0
    ```

=== "Custom Python script"

    ```bash
    conda activate geograypher
    ```

    Then run the following Python script:

    ```python
    from pathlib import Path

    import pyproj
    from geograypher.entrypoints.render_labels import render_labels

    # Change this line
    DATA_DIR = Path("path/to/data")

    # Define the inputs
    MESH_FILE = Path(DATA_DIR, "drone", "photogrammetry-outputs", "composite1_mesh.ply")
    CAMERAS_FILE = Path(DATA_DIR, "drone", "photogrammetry-outputs", "composite1_cameras.xml")
    DTM_FILE = Path(DATA_DIR, "drone", "photogrammetry-postprocessed", "full", "composite1_dtm-ptcloud.tif")
    TREE_CROWNS_FILE = Path(DATA_DIR, "detected-trees", "composite1_tree-crowns_geometric_v01.gpkg")
    IMAGE_FOLDER = Path(DATA_DIR, "drone", "raw-drone-photos", "composite1")
    MESH_CRS = pyproj.CRS.from_epsg(32610)
    ORIGNAL_IMAGE_FOLDER = "/data/raw-drone-photos"

    # Define the outputs
    RENDER_SAVEFOLDER = Path(DATA_DIR, "renders")
    LABELS_VIS_FOLDER = Path(DATA_DIR, "renders-vis")

    render_labels(
        mesh_file=MESH_FILE,
        mesh_CRS=MESH_CRS,
        cameras_file=CAMERAS_FILE,
        texture=TREE_CROWNS_FILE,
        texture_column_name="unique_ID",
        image_folder=IMAGE_FOLDER,
        render_savefolder=RENDER_SAVEFOLDER,
        original_image_folder=ORIGNAL_IMAGE_FOLDER,
        labels_vis_folder=LABELS_VIS_FOLDER,
        mesh_ROI_buffer_radius_meters=10,
        cameras_ROI_buffer_radius_meters=20,
        render_image_scale=0.125,
        DTM_file=DTM_FILE,
        ground_height_threshold=2.0,
    )
    ```

This command produces a file tree of images (in the `renders` folder) that exactly mirrors the structure of the original raw drone photos, except that instead of the original RGB images, there are single-channel images in which each pixel contains the unique ID of the tree that was observed at that pixel.

![Rendered IDs](/assets/images/tutorials/composite1_rendered-ids.png)


## Crop the view of each tree from each drone photo

The previous step identified the location of each tree in each image, but additional processing is required to prepare this data for a computer vision prediction model. Specifically, we use a _classification model_, which takes an image and produces a single label. To accommodate this format, we must create one image per view of each tree. Using the rendered mask from Geograypher, a rectangular region surrounding each observed tree is cropped from the original image. Then, any content within the crop but outside the bounds of the tree is set to a background color. Finally, each chip is written out, while preserving both the structure of the image it was derived from and the ID of the tree it was generated from.

TODO: Illustrative schematic here?

=== "Docker (recommended)"

    Linux/Mac:

    ```bash
    export DATA_DIR="path/to/data"

    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_DIR}:/data" \
        ghcr.io/open-forest-observatory/tree-classification-framework:latest \
        python -m tree_classification_framework.chip_images \
           /data/drone/raw-drone-photos/composite1 \
           /data/renders \
           /data/drone/tree-chips \
           --n-workers 4 \
           --n-chips-per-tree 10
    ```

    Windows:

    ```powershell
    $env:DATA_DIR = "path\to\data"

    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-classification-framework:latest `
        python -m tree_classification_framework.chip_images `
           /data/drone/raw-drone-photos/composite1 `
           /data/renders `
           /data/drone/tree-chips `
           --n-workers 4 `
           --n-chips-per-tree 10
    ```


=== "Python command-line entrypoint"

    ```bash
    export DATA_DIR="path/to/data"

    python -m tree_classification_framework.chip_images \
       ${DATA_DIR}/drone/raw-drone-photos/composite1 \
       ${DATA_DIR}/renders \
       ${DATA_DIR}/drone/tree-chips \
       --n-workers 4 \
       --n-chips-per-tree 10
    ```

=== "Custom Python script"

    ```bash
    conda activate tree-classification-framework
    ```

    Then run the following Python script:

    ```python
    from pathlib import Path

    from tree_classification_framework.chip_images import process_folder

    # Change this line
    DATA_DIR = Path("path/to/data")

    # Define the inputs
    IMAGE_FOLDER = Path(DATA_DIR, "drone", "raw-drone-photos", "composite1")
    RENDERS_FOLDER = Path(DATA_DIR, "renders")

    # Define the outputs
    CHIPS_FOLDER = Path(DATA_DIR, "drone", "tree-chips")

    process_folder(
        images_folder=IMAGE_FOLDER,
        renders_folder=RENDERS_FOLDER,
        output_dir=CHIPS_FOLDER,
        n_workers=4,
        n_chips_per_tree=10,
    )
    ```

This produces, in the tree-chips folder, a file tree parallelling that of the original raw drone photos, but in place of each image file is a folder. Each folder contains the cropped images of each tree that was observed in that image, with each file named with the unique numeric ID of the tree it represents.

![crop](/assets/images/tutorials/composite1_crop2_000448-02_000498.png){ width="40%" }


## Classify each crop

We can use computer vision models previously trained by the OFO to classify each chip. In this step, we'll use two independent models: one for predicting live vs. dead status and another for predicting species. The latter model is illustrative and was developed for eight common species in Sierra Nevada mixed-conifer forests. We use these models to classify each chip independently

=== "Docker (recommended)"

    !!! warning "Running without a GPU"

        If you are running this on a machine without a GPU, remove `--gpus all` from the `docker run` command below.

    Linux/Mac:

    ```bash
    export DATA_DIR="path/to/data"

    docker run --rm --user "$(id -u):$(id -g)" \
        --gpus all --group-add "$(stat -c %g /dev/nvidia0)" \
        -v "${DATA_DIR}:/data" \
        ghcr.io/open-forest-observatory/mmpretrain:latest \
        python /app/tools/predict.py \
           /data/drone/tree-chips \
           /data/cv-models/dead_live_config.py \
           /data/cv-models/dead_live_model.pth \
           /data/tree-chips-classified/classified-live-dead.json
    ```

    Windows:

    ```powershell
    $env:DATA_DIR = "path/to/data"

    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        --gpus all `
        ghcr.io/open-forest-observatory/mmpretrain:latest `
        python /app/tools/predict.py `
           /data/drone/tree-chips `
           /data/cv-models/dead_live_config.py `
           /data/cv-models/dead_live_model.pth `
           /data/tree-chips-classified/classified-live-dead.json
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

This results in one file (in JSON format) for the live/dead predictions and one for the species predictions, providing the predicted class for each image. For example:

| Image path                                                                    | Predicted class |
| ----------------------------------------------------------------------------- | --------------- |
| `/data/tree-chips-classified/000452clip/000452-01/00/000452-01_000871/00018.png` | ABCO            |
| `/data/tree-chips-classified/000452clip/000452-01/00/000452-01_000871/00090.png` | CADE27          |
| `/data/tree-chips-classified/000452clip/000452-01/00/000452-01_000871/00094.png` | CADE27          |
| `/data/tree-chips-classified/000452clip/000452-01/00/000452-01_000871/00023.png` | PILA            |

## Assign predictions to individual trees

The end goal of this process is to have geospatial, tree-level predictions. Each tree is likely to have been observed many times from different viewpoints and will therefore have multiple classification results. We maintain the tree's unique ID through all steps in the process, so the view-level predictions still tie back to a specific tree. Since predictions may differ across views, we take the modal (most common) prediction across all views, and assign this as the predicted tree label. This information is then joined with the geospatial crown information that was originally used to generate the chips, then saved out (as a new geospatial file). In addition to the predicted class, we also include the number of views which contributed to the prediction and the fraction of views that agreed with the modal prediction. These attributes are suffixed with `_n_preds` and `_frac_matching_mode`, respectively, and may be used in downstream tasks to filter out low-confidence predictions.

=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/index.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

    Linux/Mac:

    ```bash
    export DATA_DIR="path/to/data"

    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_DIR}:/data" \
        ghcr.io/open-forest-observatory/tree-classification-framework:latest \
        python -m tree_classification_framework.assign_predictions_to_trees \
           /data/tree-chips-classified/classified-live-dead.json \
           live_dead \
           /data/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
           /data/classified-trees/composite1_tree-crowns_geometric_v01_live_dead.gpkg
    ```

    Windows:

    ```powershell
    $env:DATA_DIR = "path\to\data"

    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-classification-framework:latest `
        python -m tree_classification_framework.assign_predictions_to_trees `
           /data/tree-chips-classified/classified-live-dead.json `
           live_dead `
           /data/detected-trees/composite1_tree-crowns_geometric_v01.gpkg `
           /data/classified-trees/composite1_tree-crowns_geometric_v01_live_dead.gpkg
    ```

    Note that you can run the species prediction step by replacing `live_dead` with `species` in all lines.

=== "Python command-line entrypoint"

    TODO: This can just be the TCF installation instructions I think

    ```bash
    export DATA_DIR="path/to/data"

    conda activate tree-classification-framework

    python -m tree_classification_framework.assign_predictions_to_trees \
       ${DATA_DIR}/tree-chips-classified/classified-species.json \
       species \
       ${DATA_DIR}/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
       ${DATA_DIR}/classified-trees/composite1_tree-crowns_geometric_v01_species.gpkg
    ```

    Note that you can run the species prediction step by replacing `live_dead` with `species` in all lines.

=== "Custom Python script"
    ```bash
    conda activate tree-classification-framework
    ```

    Then run the following Python script:

    ```python
    from pathlib import Path

    from tree_classification_framework.assign_predictions_to_trees import assign_predictions_to_trees

    # Change this line
    DATA_DIR = Path("path/to/data")

    # Define the inputs
    IMAGE_LEVEL_PREDICTIONS_FILE = Path(DATA_DIR, "tree-chips-classified", "classified-live-dead.json")
    TREE_CROWNS_FILE = Path(DATA_DIR, "detected-trees", "composite1_tree-crowns_geometric_v01.gpkg")

    # Define the outputs
    CLASSIFIED_CROWNS_FILE = Path(DATA_DIR, "classified-trees", "composite1_tree-crowns_geometric_v01_live_dead.gpkg")

    assign_predictions_to_trees(
        output_column_name="live_dead",
        image_level_predictions_file=IMAGE_LEVEL_PREDICTIONS_FILE,
        input_tree_crowns_file=TREE_CROWNS_FILE,
        output_tree_crowns_file=CLASSIFIED_CROWNS_FILE,
    )
    ```

    Note that you can run the species prediction step by replacing `live_dead` with `species` in all lines.

This produces a new geospatial file containing all of the attributes of the original input file, plus the prediction data.

![Detected tree crowns with species](/assets/images/tutorials/composite1_detected-crowns-w-species.png)

