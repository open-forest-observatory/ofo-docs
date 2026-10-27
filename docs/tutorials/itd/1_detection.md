---
weight: 20
---

# Task 1: Detection & mapping

We will use the OFO's [Tree Detection Framework] to detect and delineate tree crowns from drone-derived data products using a variety of approaches, including a geometric algorithm applied to a [canopy height model] (CHM) and several different computer vision algorithms applied an [orthomosaic].

## Required input data

| Name                  | Source                         | Example file                                                                                   |
| --------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------- |
| [Canopy height model] | Photogrammetry post-processing | [composite1_chm-mesh.tif](https://ucdavis.box.com/s/s02rs8rndobua45ukw0rjb8zysihicl4)          |
| [Orthomosaic]         | Photogrammetry post-processing | [composite1_ortho-dsm-ptcloud.tif](https://ucdavis.box.com/s/optcezvxz3mzeo1qshyebpnm58ab1epw) |

## Setup

Before you begin, make sure you have gone through the [OFO tutorial preparation](/tutorials/preparation.md) guidance. We recommend running OFO tools via their [Docker] images. Follow our [Docker guide](/tutorials/preparation.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers. If instead you plan to run the tools in a local Python environment, follow the local installation instructions to set up a Conda environment for the following tools:

- [Tree Detection Framework]

## Geometric tree detection from a canopy height model

First, we will use a *geometric algorithm* implemented in the Tree Detection Framework to detect treetops as local maxima in the canopy height model (CHM). This approach uses a [variable-radius local maximum filter]. We will demonstrate with the CHM linked above:

![CHM](/assets/images/tutorials/composite1_chm-mesh.png)

=== "Docker"

    Linux/Mac:

    ```bash
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_DIR}:/data" \
        ghcr.io/open-forest-observatory/tree-detection-framework:latest \
        python -m tree_detection_framework.entrypoints.detect_geometric_two_stage \
            /data/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
            /data/output/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
            --tree-crowns-save-path /data/output/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
            --raster-blur-sigma 0.5 \
            --tree-top-detector-kwargs '{"a": 0, "b": 0.0325, "c": 0.25, "min_ht": 5}'
    ```

    Windows:

    ```powershell
    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-detection-framework:latest `
        python -m tree_detection_framework.entrypoints.detect_geometric_two_stage `
            /data/photogrammetry-postprocessed/full/composite1_chm-mesh.tif `
            /data/output/detected-trees/composite1_tree-tops_geometric_v01.gpkg `
            --tree-crowns-save-path /data/output/detected-trees/composite1_tree-crowns_geometric_v01.gpkg `
            --raster-blur-sigma 0.5 `
            --tree-top-detector-kwargs '{\"a\": 0, \"b\": 0.0325, \"c\": 0.25, \"min_ht\": 5}'
    ```

=== "Jupyter"

    This step is performed by the TDF [Geometric Detector example notebook](https://github.com/open-forest-observatory/tree-detection-framework/blob/main/examples/sequential_geometric_detector.ipynb). You can change the constants in the second cell. Ensure Jupyter is using the the `tree-detection-framework` Conda environment.

    <!-- TODO: this notebook could be improved by visualizing the detected tree tops. -->

=== "Python command-line entrypoint"

    In your terminal, activate the `tree-detection-framework` Conda environment.

    ```bash
    conda activate tree-detection-framework
    ```

    Then run the [geometric detection entrypoint script](https://github.com/open-forest-observatory/tree-detection-framework/blob/main/tree_detection_framework/entrypoints/detect_geometric_two_stage.py).

    ```bash
    python -m tree_detection_framework.entrypoints.detect_geometric_two_stage \
        ${DATA_DIR}/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
        ${DATA_DIR}/output/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
        --tree-crowns-save-path ${DATA_DIR}/output/detected-trees/composite1_tree-crowns_geometric_v01.gpkg \
        --raster-blur-sigma 0.5 \
        --tree-top-detector-kwargs '{"a": 0, "b": 0.0325, "c": 0.25, "min_ht": 5}'
    ```

=== "Python script"

    Run the following code from within the `tree-detection-framework` Conda environment.

    ```python
    from pathlib import Path

    from tree_detection_framework.entrypoints.detect_geometric_two_stage import detect_trees_two_stage

    # Change this line
    DATA_DIR = Path("path/to/data")

    # Define the inputs
    CHM_PATH = Path(DATA_DIR, "photogrammetry-postprocessed", "full", "composite1_chm-mesh.tif")
    TREE_TOPS_SAVE_PATH = Path(DATA_DIR, "output", "detected-trees", "composite1_tree-tops_geometric_v01.gpkg")
    TREE_CROWNS_SAVE_PATH = Path(DATA_DIR, "output", "detected-trees", "composite1_tree-crowns_geometric_v01.gpkg")
    RASTER_BLUR_SIGMA = 0.5
    TREE_TOP_DETECTOR_KWARGS = {"a": 0, "b": 0.0325, "c": 0.25, "min_ht": 5}

    # Run detection
    detect_trees_two_stage(
        CHM_file=CHM_PATH,
        tree_tops_save_path=TREE_TOPS_SAVE_PATH,
        tree_crowns_save_path=TREE_CROWNS_SAVE_PATH,
        raster_blur_sigma=RASTER_BLUR_SIGMA,
        tree_top_detector_kwargs=TREE_TOP_DETECTOR_KWARGS,
    )
    ```

This command saves two geospatial output files: points representing detected tree tops and polygons representing detected tree crowns. You can visualize these outputs in GIS software like [QGIS]:

![CHM with detected trees](/assets/images/tutorials/composite1_chm-mesh_w-detections_geometric_v01.png)

The detected trees all have a `height` attribute extracted from the CHM by Tree Detection Framework. The heights were used to size the tree points in the visualization above.

The geometric tree detection algorithm can be parameterized in many different ways. For example, the value passed to `raster-blur-sigma` controls the amount of smoothing applied to the CHM before detecting local maxima. The values given for `a`, `b`, and `c` in the `tree-top-detector-kwargs` affects the local maximum search radius relative to the height of the tree. Other parameters not supplied here (and thus using their defaults) include `chip_size` and `chip_stride`, which control how large CHMs are split up into manageable chunks prior to processing, and `resolution`, which controls the resolution the CHM is resampled to prior to running the algorithm. See the [Tree Detection Framework documentation](https://open-forest-observatory.github.io/tree-detection-framework/command_line_usage/detect_geometric_two_stage/) for a detailed description of all parameters. Here is an example of the effect of setting the treetop detector parameter `c` to `5`.

![CHM with detected trees](/assets/images/tutorials/composite1_chm-mesh_w-detections_geometric_v02.png)

The Open Forest Observatory has done extensive testing of the geometric tree detection algorithm and has found that the default parameters used here work well in many California conifer forests. Some of our parameter tuning work is published in [Methods in Ecology and Evolution :material-open-in-new:](https://besjournals.onlinelibrary.wiley.com/doi/pdf/10.1111/2041-210X.13860){target="_blank" rel="noopener"}, and other work is in progress.

## Computer vision tree detection from an orthomosaic

The Tree Detection Framework also provides an interface to several existing computer vision models for detecting trees from an [orthomosaic]. These models run fastest when a GPU is available, but some can also run on a CPU in a reasonable amount of time, particularly for small orthomoaics.

We will first demonstrate using it to run DeepForest on the orthomosaic linked above:

![Orthomosaic](/assets/images/tutorials/composite1_ortho-dsm-ptcloud.png)

=== "Docker"

    !!! warning "Running without a GPU"

        If you are running this on a machine without a GPU, remove `--gpus all` from the `docker run` command below.

    Linux/Mac:

    ```bash
    docker run --rm --user "$(id -u):$(id -g)" \
        --gpus all  --group-add "$(stat -c %g /dev/nvidia0)" \
        -v "$DATA_DIR:/data" \
        ghcr.io/open-forest-observatory/tree-detection-framework:latest \
        python -m tree_detection_framework.entrypoints.generate_predictions \
            --raster-folder-path /data/photogrammetry-postprocessed/full/composite1_ortho-dsm-ptcloud.tif \
            --tree-detection-model deepforest \
            --chip-size 1024 \
            --chip-stride 768 \
            --resolution 0.05 \
            --run-nms \
            --predictions-save-path /data/output/detected-trees/composite1_tree-crowns_deepforest-bbox_v01.gpkg
    ```

    Windows:

    ```powershell
    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-detection-framework:latest `
        python -m tree_detection_framework.entrypoints.generate_predictions `
            --raster-folder-path /data/photogrammetry-postprocessed/full/composite1_ortho-dsm-ptcloud.tif `
            --tree-detection-model deepforest `
            --chip-size 1024 `
            --chip-stride 768 `
            --resolution 0.05 `
            --run-nms `
            --predictions-save-path /data/output/detected-trees/composite1_tree-crowns_deepforest-bbox_v01.gpkg
    ```

=== "Jupyter"

    This step is performed by the TDF [tree detection example notebook](https://github.com/open-forest-observatory/tree-detection-framework/blob/main/examples/predict_detections.ipynb). Note that the constants in cell 2 will need to be changed to reflect the data used in this documentation. Ensure Jupyter is using the the `tree-detection-framework` Conda environment.

=== "Python command-line entrypoint"

    In your terminal, activate the `tree-detection-framework` Conda environment.

    ```bash
    conda activate tree-detection-framework
    ```

    Then run the [prediction generation entrypoint script](https://github.com/open-forest-observatory/tree-detection-framework/blob/main/tree_detection_framework/entrypoints/generate_predictions.py).

    ```bash
    python -m tree_detection_framework.entrypoints.generate_predictions \
        --raster-folder-path ${DATA_DIR}/photogrammetry-postprocessed/full/composite1_ortho-dsm-ptcloud.tif \
        --tree-detection-model deepforest \
        --chip-size 1024 \
        --chip-stride 768 \
        --resolution 0.05 \
        --run-nms \
        --predictions-save-path ${DATA_DIR}/output/detected-trees/composite1_tree-crowns_deepforest-bbox_v01.gpkg
    ```

    Note that you can replace `deepforest` with `detectree2` to run that model.

=== "Python script"

    Run the following code from within the `tree-detection-framework` Conda environment.

    ```python
    from pathlib import Path

    from tree_detection_framework.entrypoints.generate_predictions import (
        generate_predictions,
    )

    # Change this line
    DATA_DIR = Path("path/to/data")

    # Define the inputs
    RASTER_FOLDER_PATH = Path(DATA_DIR, "photogrammetry-postprocessed", "full", "composite1_ortho-dsm-ptcloud.tif")
    TREE_DETECTION_MODEL = "deepforest"
    CHIP_SIZE = 1024
    CHIP_STRIDE = 768
    RESOLUTION = 0.05
    RUN_NMS = True

    # Define the outputs
    PREDICTIONS_SAVE_PATH = Path(DATA_DIR, "output", "detected-trees", "composite1_tree-crowns_deepforest-bbox_v01.gpkg")

    # Run detection
    generate_predictions(
        raster_folder_path=RASTER_FOLDER_PATH,
        predictions_save_path=PREDICTIONS_SAVE_PATH,
        tree_detection_model=TREE_DETECTION_MODEL,
        chip_size=CHIP_SIZE,
        chip_stride=CHIP_STRIDE,
        resolution=RESOLUTION,
        run_nms=RUN_NMS,
    )
    ```

This step saves a geospatial file of polygons (rectangles) representing the bounding boxes of detected tree crowns. You can visualize these outputs in GIS software like [QGIS]:

![CHM with detected trees](/assets/images/tutorials/composite1_chm-mesh_w-detections_deepforest-bbox_v01.png)

The rectangle bounding box output format is specific to the DeepForest model.

Since geospatial rasters are often large, we cannot assume that a computer vision model can generate predictions for the whole raster at once. Instead, the raster is broken up into smaller chips, and an independent prediction is generated on each one. These predictions are subsequently merged back together. The `chip_size` and `chip_stride` parameters, both in pixels, represent the chip dimensions and how much the sliding window moves between each chip. The computer vision models may produce overlapping detections, and the `run_nms` argument controls whether the non-max suppression algorithm should be run to only retain the highest-confidence detection if multiple overlap. Finally, the `resolution` parameter controls the size in meters of a single pixel in the chip, and the original data is resampled on the fly to achieve this. In practice, this parameter has a large impact on the performance of models and specifically what size of tree is detected well. By coarsening the resolution to `0.2m`, only the largest trees are detected, as visualized below.

<!-- TODO DR: consider visualizing a chip from each resolution. -->

![Ortho with deepforest detections from low-res chips](/assets/images/tutorials/composite1_ortho_w-detections_deepforest-bbox_v01_low-res.png)

The Tree Detection Framework provides a standardized interface to several different methods of performing tree detection, taken from the literature. TDF handles the process of chipping a raster into smaller chips, generating predictions on each chip, and merging these predictions back together in one command, so this complexity is abstracted from the user, and end-to-end workflows are easy to run. A key benefit of TDF is the ability to quickly compare multiple models, while holding key pre- and post-processing parameters consistent. TDF is also optimized for realistic-scale raster data, meaning that it can be directly applied to even the largest drone flights. A table of the supported approaches is below.

| Method | Learning Strategy | Input Data | Output Format |
| --- | --- | --- | --- |
| DeepForest | Task-specific training | Orthomosaic | Bounding box |
| Detectree2 | Task-specific training | Orthomosaic | Crown polygon |
| Restor TCD | Task-specific training | Orthomosaic | Crown polygon |
| Segment Anything Model v2 (SAM2) | Generic pretraining (foundational model) | Orthomosaic | Crown polygon |
| Segment Anything Model v3 (SAM3) | Generic pretraining, with class information (foundational model) | Orthomosaic | Crown polygon |
| Local maximum filter + Watershed segmentation | Learning-free algorithm | Canopy height model (CHM) | Tree-top point and crown polygon |

To run detections using an alternative model, simply change `deepforest` in the command above to the name of the model you want to use.

<!-- For example, here we have changed it to `detectree2`. (TODO: Add visualization of Detectree2 output.) -->

To enable support for SAM3, you must follow the prompts [here](https://huggingface.com/facebook/sam3). This will require you to create a HuggingFace account if you do not have one already. After creating an account, you must wait for your request to be manually reviewed. Then go [here](https://huggingface.co/settings/tokens), select `Create new token`, and select Token type `Read`. Enter an arbitrary name and create the token. Copy the token and store it somewhere, since you won't be able to see its value after creating it. Finally, add it to the list of arguments when running the SAM3 model:

```bash
--sam3-huggingface-token SAM3_HUGGINGFACE_TOKEN
```

## Generating tree top points from computer vision detections

The computer vision tree detection approaches do not product a point representation of trees by default. However, tree top points are required for matching detected trees to ground reference trees, as demonstrated in the [Evaluation](/tutorials/itd-eval/) tutorial. TDF provides a tool to generate tree top points from computer vision crown polygons.

=== "Docker"

    Linux/Mac:

    ```bash
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "$DATA_DIR:/data" \
        ghcr.io/open-forest-observatory/tree-detection-framework:latest \
        python -m tree_detection_framework.entrypoints.polygons_to_points \
            --detections-path /data/detected-trees/composite1_tree-crowns_deepforest-bbox_v01.gpkg \
            --chm-path /data/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
            --output-path /data/output/detected-trees/composite1_tree-crowns_deepforest-bbox_v01-tree_points_chm-max.gpkg \
            --method chm_max
    ```

    Windows:

    ```powershell
    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-detection-framework:latest `
        python -m tree_detection_framework.entrypoints.polygons_to_points `
            --detections-path /data/detected-trees/composite1_tree-crowns_deepforest-bbox_v01.gpkg `
            --chm-path /data/photogrammetry-postprocessed/full/composite1_chm-mesh.tif `
            --output-path /data/output/detected-trees/composite1_tree-crowns_deepforest-bbox_v01-tree_points_chm-max.gpkg `
            --method chm_max
    ```

=== "Python command-line entrypoint"

    In your terminal, activate the `tree-detection-framework` Conda environment.

    ```bash
    conda activate tree-detection-framework
    ```

    Then run the [polygons to points script](https://github.com/open-forest-observatory/tree-detection-framework/blob/main/tree_detection_framework/entrypoints/polygons_to_points.py) script.

    ```bash
    python -m tree_detection_framework.entrypoints.polygons_to_points \
        --detections-path ${DATA_DIR}/detected-trees/composite1_tree-crowns_deepforest-bbox_v01.gpkg \
        --chm-path ${DATA_DIR}/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
        --output-path ${DATA_DIR}/output/detected-trees/composite1_tree-crowns_deepforest-bbox_v01-tree_points_chm-max.gpkg \
        --method chm_max
    ```

=== "Python script"

    Run the following code from within the `tree-detection-framework` Conda environment.

    ```python
    from pathlib import Path

    from tree_detection_framework.entrypoints.polygons_to_points import (
        polygons_to_points,
    )

    # Change this line
    DATA_DIR = Path("path/to/data")

    DETECTIONS_DIR = Path(DATA_DIR, "detected-trees", "composite1_tree-crowns_deepforest-bbox_v01.gpkg")
    CHM_PATH = Path(DATA_DIR, "photogrammetry-postprocessed", "full", "composite1_chm-mesh.tif")
    OUTPUT_PATH = Path(DATA_DIR, "output", "detected-trees", "composite1_tree-crowns_deepforest-bbox_v01-tree_points_chm-max.gpkg")
    METHOD = "chm_max"

    polygons_to_points(
        detections_path = DETECTIONS_DIR,
        output_path = OUTPUT_PATH,
        method = METHOD,
        chm_path = CHM_PATH,
    )
    ```
This saves a geospatial file of points representing the detected tree tops, with heights extracted from the CHM.

![CHM-derived points](/assets/images/tutorials/composite1_detected-crowns_chm-max.png).

In this example, the highest CHM point within each detection polygon is selected as the tree top. Alternatively, this approach can be replaced with simply selecting the centroid, by replacing the `chm_max` method with `centroid`. In either case, the height is extracted from the corresponding point on the CHM, if provided.

For a full description of the TDF computer vision tree detection module and its options, see the [Tree Detection Framework documentation](https://open-forest-observatory.github.io/tree-detection-framework/command_line_usage/generate_predictions/).
