---
weight: 20
---

# Task 2: Evaluation

The final task is assessing the quality of the detected trees. This is done by comparing the locations of detected trees to those of spatially-shifted field reference trees. This process produces precision, recall, and F1 scores for the tree detection task.

## Required input data

| Name                  | Source                         | Example file                                                                                   |
| --------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------- |
| Ground reference trees | Manual field work             | [ofo-ground-reference-trees_0030.gpkg](https://ucdavis.box.com/s/4z4j3npqbdwx2p24mv2zriw3zm1xlfbn)          |
| Detected trees         | Tree detection algorithm      | [composite1_tree-tops_geometric_v01.gpkg](TODO)          |
| Registration file      | Registration algorithm        | [ofo-ground-reference-trees_0030_shifted.gpkg](TODO)          |

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

## Detection evaluation with height-dependent matching threshold

The tree detection scoring algorithm operates on the ground reference and drone-predicted trees, both represented as sets points with associated height information. A drone tree can match a field tree if it is within a variable threshold distance, based on the field tree height. This threshold is defined as 0.1 the height of the field tree plus 1m. This approach is described in [Methods in Ecology and Evolution :material-open-in-new:](https://besjournals.onlinelibrary.wiley.com/doi/pdf/10.1111/2041-210X.13860){target="_blank" rel="noopener"}. Spatial error may mean that threshold distance criteria allows matches that are not one-to-one, so the final one-to-one matching is constructed by pairing the trees with the minimum distance satisfying the threshold criteria and then removing both paired trees from consideration. This process repeats until all tree pairs with a threshold-satisfying distance are matched. The scoring process is restricted to the region 5m away from the plot bounds, to ensure that no spatial edge-effects occur, and to field trees over 10m in height.

An example of the matched trees is shown below. Note that for tree pairs that are very well aligned it may be hard to see the black line indicating they are paired.
![matched trees](/assets/images/tutorials/tree-scoring-matches.png)

For this example, the following metric values were obtained:

| Metric   | Value    |
| -------- | -------- |
| Precision|  1.0     |
| Recall   |  0.73    |
| F1       |  0.84    |

=== "Docker"

    Linux/Mac:

    ```bash
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"

    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_FOLDER}:/data" \
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest \
        python -m tree_registration_and_matching.entrypoints.score_detected_trees \
            /data/inputs/ground-reference/ofo-ground-reference-trees_0030.gpkg \
            /data/outputs/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
            /data/inputs/ground-reference/ofo-ground-reference-plot_0030.gpkg \
            --shift-file /data/intermediate/registration/reference-drone-registration.csv  \
            --output-file /data/outputs/detection-evaluation/tree-scoring-metrics.json \
            --vis-file /data/outputs/detection-evaluation/tree-scoring-matches.png
    ```

    Windows: TODO

    ```powershell
    ```

=== "Jupyter"

    This step is performed by lines XX-YY (TODO) of the Jupyter notebook {TODO: Link to notebook}.

=== "Python command-line entrypoint"

    ```bash
    export DATA_FOLDER="path/to/data"

    python -m tree_registration_and_matching.entrypoints.score_detected_trees \
        ${DATA_FOLDER}/inputs/ground-reference/ofo-ground-reference-trees_0030.gpkg \
        ${DATA_FOLDER}/outputs/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
        ${DATA_FOLDER}/inputs/ground-reference/ofo-ground-reference-plot_0030.gpkg \
        --shift-file ${DATA_FOLDER}/intermediate/registration/reference-drone-registration.csv  \
        --output-file /data/outputs/detection-evaluation/tree-scoring-metrics.json \
        --vis-file ${DATA_FOLDER}/outputs/detection-evaluation/tree-scoring-matches.png
    ```

=== "Python script"

    ```python
    # TODO write out the appropriate parts of the entrypoint here:
    # https://github.com/open-forest-observatory/tree-registration-and-matching/blob/4246c5185833061989c91314eddec71d28cafb19/tree_registration_and_matching/entrypoints/match_field_attributes_to_drone.py#L15
    ```