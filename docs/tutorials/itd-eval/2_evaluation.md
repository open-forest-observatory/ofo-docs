---
weight: 20
---

# Task 2: Evaluation

The final task is assessing the quality of the detected trees. This is done by comparing the locations of detected trees to those of field reference trees after co-registering the datasets ([Registration](/tutorials/itd-eval/1_registration.md) task). This process produces metrics quantifying the fraction of real trees the detection algorithm found ("recall"), the fraction of detected trees that were real ("precision"), and a combined metric (F1) that balances the two. The evaluation process also produces a visualization of the matched trees, which can be used to identify patterns in the errors made by the detection algorithm.

## Required input data

| Name                   | Source                   | Example file                                                                                          |
| ---------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------- |
| Ground reference trees | Manual field work        | [ofo-ground-reference-trees_0030.gpkg](https://ucdavis.box.com/s/4z4j3npqbdwx2p24mv2zriw3zm1xlfbn)    |
| Detected trees         | Tree detection algorithm | [composite1_tree-tops_geometric_v01.gpkg](https://ucdavis.box.com/s/tese51t1g97a3jb3f67iaohefftkg5cn) |
| Registration file      | Registration algorithm   | [reference-drone-registration.csv](https://ucdavis.box.com/s/r7k8iuduhxwulf5u1osydhuf8ohaqhbv)        |

The detected tree crowns and registration file may be ones you produced in the [Detection](/tutorials/itd/1_detection.md) and [Registration](/tutorials/itd-eval/1_registration.md) tasks, respectively, or you can use the pre-generated files in the tutorial data folder (linked above). You may similarly provide your own ground reference trees file, as long as it contains an attribute named `height` for each tree, or use the pre-prepared file in the tutorial data folder.

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

## Detection evaluation with spatial tolerance

The tree detection evaluation algorithm quantifies how well the detected trees correspond to the ground reference trees. Does every detected tree correspond to a real tree observed on the ground? Does every real tree have a corresponding detected tree? To answer these quetions, we need to pair the detected trees with their corresponding ground reference trees. However, due to random spatial error in both the drone and ground reference datasets, corresponding trees are never exactly co-located. Therefore, we allow a spatial tolerance in determining whether a detected tree corresponds to a ground reference tree. The spatial tolerance is a function of the height of the ground reference tree, with taller trees having a larger tolerance. This approach, published in [Methods in Ecology and Evolution :material-open-in-new:](https://besjournals.onlinelibrary.wiley.com/doi/pdf/10.1111/2041-210X.13860){target="_blank" rel="noopener"}, accounts for the fact that taller trees are morely likely to have a lean or complex crown morphology such that the tree top (the point detected by drone) is not directly above the stem (the point mapped in the ground survey).

The spatial tolerance could, in some cases, allow a given ground tree to match to more than one drone tree or vice-versa. To avoid this, the algorithm uses a greedy matching approach which identifies the best (spatially closest) match between the two datasets, then removes those trees from further matching, then computes the next best match, and so on until all trees have been matched or no more matches can be made.

Once all matchable trees are matched, it is then possible to compute the evaluation metrics based on the number of trees and the number that were matched, in both the drone and ground datasets. When scoring, it is necessary to exclude spatial edge effects (e.g. a drone tree just inside the plot bounds that corresponded to a real field tree that was just outside the plot bounds and was therefore not recorded). To account for this, the scoring process only asks about matches for trees that are inset at least 5 m from the plot bounds, and which are over 10 m in height.

The commands to run this algorithm are shown below.

=== "Docker"

    Linux/Mac:

    ```bash
    export DATA_FOLDER="path\to\data"

    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_FOLDER}:/data" \
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest \
        python -m tree_registration_and_matching.entrypoints.score_detected_trees \
            /data/ground-reference/ofo-ground-reference-trees_0030.gpkg \
            /data/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
            /data/ground-reference/ofo-ground-reference-plot_0030.gpkg \
            --shift-file /data/registration/reference-drone-registration.csv  \
            --output-file /data/detection-evaluation/tree-scoring-metrics.json \
            --vis-file /data/detection-evaluation/tree-scoring-matches.png
    ```

    Windows:

    ```powershell
    $env:DATA_DIR = "path\to\data"

    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest `
        python -m tree_registration_and_matching.entrypoints.score_detected_trees `
            /data/ground-reference/ofo-ground-reference-trees_0030.gpkg `
            /data/detected-trees/composite1_tree-tops_geometric_v01.gpkg `
            /data/ground-reference/ofo-ground-reference-plot_0030.gpkg `
            --shift-file /data/registration/reference-drone-registration.csv `
            --output-file /data/detection-evaluation/tree-scoring-metrics.json `
            --vis-file /data/detection-evaluation/tree-scoring-matches.png
    ```

=== "Jupyter"

    This step is performed by lines XX-YY (TODO) of the Jupyter notebook {TODO: Link to notebook}.

=== "Python command-line entrypoint"

    ```bash
    export DATA_FOLDER="path/to/data"

    python -m tree_registration_and_matching.entrypoints.score_detected_trees \
        ${DATA_FOLDER}/ground-reference/ofo-ground-reference-trees_0030.gpkg \
        ${DATA_FOLDER}/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
        ${DATA_FOLDER}/ground-reference/ofo-ground-reference-plot_0030.gpkg \
        --shift-file ${DATA_FOLDER}/registration/reference-drone-registration.csv  \
        --output-file ${DATA_FOLDER}/detection-evaluation/tree-scoring-metrics.json \
        --vis-file ${DATA_FOLDER}/detection-evaluation/tree-scoring-matches.png
    ```

=== "Python script"

    ```python
    # TODO write out the appropriate parts of the entrypoint here:
    # https://github.com/open-forest-observatory/tree-registration-and-matching/blob/4246c5185833061989c91314eddec71d28cafb19/tree_registration_and_matching/entrypoints/match_field_attributes_to_drone.py#L15
    ```

This saves out a map image depicting the detected and reference trees and the matches between them. Ground reference trees are indicated in light blue, drone-detected trees are in red, and the matches between them are in pink. The plot bounds are shown in white.

![matched trees](/assets/images/tutorials/tree-scoring-matches.png)

It also saves out a JSON file containing the evaluation metrics. For the example here:

| Metric   | Value    |
| -------- | -------- |
| Precision|  1.0     |
| Recall   |  0.73    |
| F1       |  0.84    |
