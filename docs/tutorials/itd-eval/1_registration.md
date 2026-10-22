---
weight: 20
---

# Task 1: Co-registration

For many applications, we may wish to compare the results of drone-based tree detection and classification against ground reference data. However, before we can do any comparison, we need to make sure the two datasets are spatially co-registered (aligned).

## Required input data

| Name                   | Source                         | Example file                                                                                       |
| ---------------------- | ------------------------------ | -------------------------------------------------------------------------------------------------- |
| [Canopy height model]  | Photogrammetry post-processing | [composite1_chm-mesh.tif](https://ucdavis.box.com/s/s02rs8rndobua45ukw0rjb8zysihicl4)              |
| Ground reference trees (geospatial points) | Manual fieldwork              | [ofo-ground-reference-trees_0030.gpkg](https://ucdavis.box.com/s/4z4j3npqbdwx2p24mv2zriw3zm1xlfbn) |

## Setup

!!! info "Before you begin"

    Make sure you have gone through the [OFO tutorial preparation](/tutorials/index.md#preparing-to-follow-the-tutorials) guidance.

=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/index.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

=== "Jupyter"

    TODO: Link to the notebook we will be using, info to set up Conda env as for the other Python options?

=== "Python command-line entrypoint"

    Install the Tree Registration and Matching library and its dependencies following the [installation instructions](https://github.com/open-forest-observatory/tree-registration-and-matching/tree/main#install).

=== "Python script"

    Install the Tree Registration and Matching library and its dependencies following the [installation instructions](https://github.com/open-forest-observatory/tree-registration-and-matching/tree/main#install).

     Then load the required libraries:

    ```python
    # TODO: Complete python lines to load libraries
    ```

## Registration using height correlation

While both the drone imagery and reference tree locations are usually georeferenced with GPS/GNSS, each set of measurements can have an independent bias due to GPS/GNSS error (e.g., atmospheric distortions, signal attenuation by the tree canopy) a the time of survey. This creates a spatial offset, commonly on the order of several meters, between the two sets of data. An example of this phenomenon can be seen below, where the field reference trees (blue points) are shifted upward and slightly left relative to the corresponding drone trees represented by the CHM. The white line represents the bounds of of the ground plot, showing the region within which trees were surveyed.

![initial registration](/assets/images/tutorials/registration-initial.png)

The OFO has developed the [Tree Registration and Matching Toolkit](https://github.com/open-forest-observatory/tree-registration-and-matching) (TRAM) to automatically identify the spatial registration between two datasets. The specific algorithm we will be using here registers a set of ground reference trees (geospatial points) to a drone-derived [CHM] (a geospatial raster). TRAM also contains algorithms to register two sets of geospatial points (e.g., ground reference trees and drone-detected trees).

The algorithm use will use to align the drone and reference data takes the CHM and ground reference tree locations (with a `height` attribute for each tree) as input. The algorithm extracts the height value from the CHM at each reference tree location, then computes the correlation between the reference tree heights and the CHM-derived heights. It then shifts the reference tree locations across a grid of offsets in both the x and y directions, and at each offset, re-computes the height correlation. The result is a grid of correlation values, where the maximum correlation indicates the optimal shift to align the two datasets.

The commands to run this algorithm are below.

=== "Docker"

    Linux/Mac:

    ```bash
    export DATA_FOLDER="path/to/data/"
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_FOLDER}:/data" \
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest \
        python -m tree_registration_and_matching.entrypoints.register_trees_to_CHM \
            --CHM-file /data/drone/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
            --tree-points-file /data/ground-reference/ofo-ground-reference-trees_0030.gpkg \
            --output-shifted-trees /data/registration/ofo-ground-reference-trees_0030_shifted.gpkg \
            --output-shift-summary /data/registration/reference-drone-registration.csv
    ```

    Windows:

    ```powershell
    $env:DATA_DIR = "path\to\data"

    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest `
        python -m tree_registration_and_matching.entrypoints.register_trees_to_CHM `
            --CHM-file /data/drone/photogrammetry-postprocessed/full/composite1_chm-mesh.tif `
            --tree-points-file /data/ground-reference/ofo-ground-reference-trees_0030.gpkg `
            --output-shifted-trees /data/registration/ofo-ground-reference-trees_0030_shifted.gpkg `
            --output-shift-summary /data/registration/reference-drone-registration.csv
    ```

=== "Jupyter"

    This step is performed by lines XX-YY (TODO) of the Jupyter notebook {TODO: Link to notebook}.

=== "Python command-line entrypoint"

    ```bash
    export DATA_FOLDER="path/to/data/"

    python -m tree_registration_and_matching.entrypoints.register_trees_to_CHM \
        --CHM-file ${DATA_FOLDER}/drone/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
        --tree-points-file ${DATA_FOLDER}/ground-reference/ofo-ground-reference-trees_0030.gpkg \
        --output-shifted-trees ${DATA_FOLDER}/registration/ofo-ground-reference-trees_0030_shifted.gpkg \
        --output-shift-summary ${DATA_FOLDER}/registration/reference-drone-registration.csv
    ```

=== "Python script"

    ```python
    # TODO write out the appropriate parts of the entrypoint here:
    # https://github.com/open-forest-observatory/tree-registration-and-matching/blob/4246c5185833061989c91314eddec71d28cafb19/tree_registration_and_matching/entrypoints/match_field_attributes_to_drone.py#L15
    ```

This algorithm identifies the optimal shift and saves out a CSV file that describes the shift, including diagnostic metrics that can be used to interpret whether the result is likely to be correct.

| estimated_shift_x | estimated_shift_y | shift_CRS  | optimal_correlation | ratio_quality_metric | n_shift_trees | CHM_file                | average_error_frac |
| ----------------- | ----------------- | ---------- | ------------------- | -------------------- | ------------- | ----------------------- | ------------------ |
| 1.0               | -4.2              | EPSG:32610 | 0.6992              | 0.7261               | 31            | composite1_chm-mesh.tif | 0.1958             |

It also saves a shifted copy of the original reference trees as a geospatial point file that is otherwise identical to the original.

![final registration](/assets/images/tutorials/registration-final.png)

Note that now the surveyed tree tops match up much better with the drone CHM. While there are some errors, these errors are in different directions for every tree, so no single shift would improve all trees dramatically. Some small amount of tree-level error is always expected, due largely to human error during ground survey and the fact that ground surveyed tree locations (tree stems) are not always directly under the tree tops. In the next task, we will see that despite these errors, we can use a simple matching algorithm to identify the tree-to-tree correspondences between the two datasets.
