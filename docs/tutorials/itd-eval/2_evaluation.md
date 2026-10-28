---
weight: 20
---

# Task 2: Evaluation

The final task is assessing the quality of the detected trees. This is done by comparing the locations of detected trees to those of field reference trees after co-registering the datasets ([Registration](/tutorials/itd-eval/1_registration.md) task). This process produces metrics quantifying the fraction of real trees the detection algorithm found ("recall"), the fraction of detected trees that were real ("precision"), and a combined metric (F1) that balances the two. The evaluation process also produces a visualization of the matched trees, which can be used to identify patterns in the errors made by the detection algorithm.

## Required input data

| Name                   | Source                   | Example file                                                                                          |
| ---------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------- |
| Ground reference trees | Manual field work        | [ofo-ground-reference-trees_0030.gpkg](https://ucdavis.box.com/s/4z4j3npqbdwx2p24mv2zriw3zm1xlfbn)    |
| Ground reference plot  | Manual field work        | [ofo-ground-reference-plot_0030.gpkg](https://ucdavis.box.com/s/dqhxw2k5jh8g7649pojnqa3ul3nrmpm1)    |
| Detected trees         | Tree detection algorithm | [composite1_tree-tops_geometric_v01.gpkg](https://ucdavis.box.com/s/tese51t1g97a3jb3f67iaohefftkg5cn) |
| Registration file      | Registration algorithm   | [reference-drone-registration.csv](https://ucdavis.box.com/s/r7k8iuduhxwulf5u1osydhuf8ohaqhbv)        |
| Classified tree tops      | Classification workflow   | [composite1_tree-tops_geometric_v01_species.gpkg](https://ucdavis.box.com/s/5kzc7lml8oz7kld90jxflm3isbok1yay)        |

The detected tree crowns and registration file may be ones you produced in the [Detection](/tutorials/itd/1_detection.md) and [Registration](/tutorials/itd-eval/1_registration.md) tasks, respectively, or you can use the pre-generated files in the tutorial data folder (linked above). You may similarly provide your own ground reference trees file, as long as it contains an attribute named `height` for each tree, or use the pre-prepared file in the tutorial data folder.

## Setup

Before you begin, make sure you have gone through the [OFO tutorial preparation](/tutorials/preparation.md) guidance. We recommend running OFO tools via their [Docker] images. Follow our [Docker guide](/tutorials/preparation.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers. If instead you plan to run the tools in a local Python environment, follow the local installation instructions to set up a Conda environment for the following tools:

- [Tree Registration and Matching Toolkit]

## Detection evaluation with spatial tolerance

The tree detection evaluation algorithm quantifies how well the detected trees correspond to the ground reference trees. Does every detected tree correspond to a real tree observed on the ground? Does every real tree have a corresponding detected tree? To answer these questions, we need to pair the detected trees with their corresponding ground reference trees. However, due to random spatial error in both the drone and ground reference datasets, corresponding trees are never exactly co-located. Therefore, we allow a spatial tolerance in determining whether a detected tree corresponds to a ground reference tree. The spatial tolerance is a function of the height of the ground reference tree, with taller trees having a larger tolerance. This approach, published in [Methods in Ecology and Evolution :material-open-in-new:](https://besjournals.onlinelibrary.wiley.com/doi/pdf/10.1111/2041-210X.13860){target="_blank" rel="noopener"}, accounts for the fact that taller trees are morely likely to have a lean or complex crown morphology such that the tree top (the point detected by drone) is not directly above the stem (the point mapped in the ground survey).

The spatial tolerance could, in some cases, allow a given ground tree to match to more than one drone tree or vice-versa. To avoid this, the algorithm uses a greedy matching approach which identifies the best (spatially closest) match between the two datasets, then removes those trees from further matching, then computes the next best match, and so on until all trees have been matched or no more matches can be made.

Once all matchable trees are matched, it is then possible to compute the evaluation metrics based on the number of trees and the number that were matched, in both the drone and ground datasets. When scoring, it is necessary to exclude spatial edge effects (e.g. a drone tree just inside the plot bounds that corresponded to a real field tree that was just outside the plot bounds and was therefore not recorded). To account for this, the scoring process only asks about matches for trees that are inset at least 5 m from the plot bounds, and which are over 10 m in height.

The commands to run this algorithm are shown below.

=== "Docker"

    Linux/Mac:

    ```bash
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_DIR}:/data" \
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest \
        python -m tree_registration_and_matching.entrypoints.score_detected_trees \
            /data/ground-reference/ofo-ground-reference-trees_0030.gpkg \
            /data/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
            /data/ground-reference/ofo-ground-reference-plot_0030.gpkg \
            --shift-file /data/registration/reference-drone-registration.csv \
            --output-file /data/output/detection-evaluation/tree-scoring-metrics.json \
            --vis-file /data/output/detection-evaluation/tree-scoring-matches.png
    ```

    Windows:

    ```powershell
    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest `
        python -m tree_registration_and_matching.entrypoints.score_detected_trees `
            /data/ground-reference/ofo-ground-reference-trees_0030.gpkg `
            /data/detected-trees/composite1_tree-tops_geometric_v01.gpkg `
            /data/ground-reference/ofo-ground-reference-plot_0030.gpkg `
            --shift-file /data/registration/reference-drone-registration.csv `
            --output-file /data/output/detection-evaluation/tree-scoring-metrics.json `
            --vis-file /data/output/detection-evaluation/tree-scoring-matches.png
    ```

=== "Python command-line entrypoint"

    In your terminal, activate the `tree-registration-and-matching` Conda environment.

    ```bash
    conda activate tree-registration-and-matching
    ```

    Then run the [tree detection scoring entrypoint script](https://github.com/open-forest-observatory/tree-registration-and-matching/blob/main/tree_registration_and_matching/entrypoints/score_detected_trees.py).

    ```bash
    python -m tree_registration_and_matching.entrypoints.score_detected_trees \
        ${DATA_DIR}/ground-reference/ofo-ground-reference-trees_0030.gpkg \
        ${DATA_DIR}/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
        ${DATA_DIR}/ground-reference/ofo-ground-reference-plot_0030.gpkg \
        --shift-file ${DATA_DIR}/registration/reference-drone-registration.csv \
        --output-file ${DATA_DIR}/output/detection-evaluation/tree-scoring-metrics.json \
        --vis-file ${DATA_DIR}/output/detection-evaluation/tree-scoring-matches.png
    ```

=== "Python script"

    Run the following code from within the `tree-registration-and-matching` Conda environment.

    ```python
    from pathlib import Path

    from tree_registration_and_matching.entrypoints.score_detected_trees import score_detected_trees

    # Change this line
    DATA_DIR = Path("path/to/data")

    # Define the inputs
    FIELD_TREES_FILE = Path(DATA_DIR, "ground-reference", "ofo-ground-reference-trees_0030.gpkg")
    DRONE_TREES_FILE = Path(DATA_DIR, "detected-trees", "composite1_tree-tops_geometric_v01.gpkg")
    FIELD_PLOT_BOUNDS_FILE = Path(DATA_DIR, "ground-reference", "ofo-ground-reference-plot_0030.gpkg")
    SHIFT_FILE = Path(DATA_DIR, "registration", "reference-drone-registration.csv")

    # Define the outputs
    OUTPUT_FILE = Path(DATA_DIR, "output", "detection-evaluation", "tree-scoring-metrics.json")
    VIS_FILE = Path(DATA_DIR, "output", "detection-evaluation", "tree-scoring-matches.png")

    metrics = score_detected_trees(
        field_trees_file=FIELD_TREES_FILE,
        drone_trees_file=DRONE_TREES_FILE,
        field_plot_bounds_file=FIELD_PLOT_BOUNDS_FILE,
        shift_file=SHIFT_FILE,
        output_file=OUTPUT_FILE,
        vis_file=VIS_FILE,
    )
    print(metrics)
    ```

This command saves out a map image depicting the detected and reference trees and the matches between them.
![matched trees TRAM](/assets/images/tutorials/tree-scoring-matches-from-TRAM.png)

The lines denoting the matches can also be saved out as a geospatial file using the `--matches-file` flag so the same figure can be recreated in `QGIS` or similar, potentially with other layers included. In this case, the matches are shown overlayed on the CHM.

![matched trees](/assets/images/tutorials/tree-scoring-matches.png){width="60%"}

Finally, this tool saves out a JSON file containing the evaluation metrics. For the example here:

| Metric   | Value    |
| -------- | -------- |
| Precision|  1.0     |
| Recall   |  0.73    |
| F1       |  0.84    |

## Attribute prediction evaluation
In many applications, the goal is to not only detect trees but also predict an attribute of them. In earlier sections of the tutorial, we presented examples of adding height information to detection trees from a CHM or generating species or live/dead predictions using computer vision. To assess the quality of these predictions, we must compare the predicted values to ground reference values. This can be done by following the procedure above to match ground- and drone-derived trees, and then comparing the predicted and observed attributes. The same tool which scores detection quality can also be used for assessing attribute prediction quality, using additional flags. This works for both continuous and categorical data, with different visualizations and metrics for each.

The `--scoring-metrics-savefile` flag controls where a `.json` file of metrics is written out, evaluating the quality of the predictions. The `--predicted-attribute-savefile` controls where a `.csv` file is written, which has one line for every field tree, and a column for both the field-derived attribute and the drone-derived attribute from the matching tree. Note that some rows may lack a drone derived attribute if that field tree was not matched to a drone tree.
The final major output is a visualization of the attribute, controlled by the `--vis-attribute-scoring-savefile` flag.
Below is a visualization of the drone-derived tree heights plotted against the field-derived heights for the corresponding trees.
![evaluating height predictions](/assets/images/tutorials/composite1_height_scoring.png)

The following example shows how to score the height predictions.

=== "Docker"

    Linux/Mac:

    ```bash
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_DIR}:/data" \
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest \
        python -m tree_registration_and_matching.entrypoints.score_detected_trees \
            /data/ground-reference/ofo-ground-reference-trees_0030.gpkg \
            /data/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
            /data/ground-reference/ofo-ground-reference-plot_0030.gpkg \
            --shift-file /data/registration/reference-drone-registration.csv \
            --field-attribute-to-score height \
            --drone-attribute-to-score height \
            --continuous-scoring-attribute \
            --scoring-metrics-savefile /data/output/detection-evaluation/height-scoring-metrics.json \
            --vis-attribute-scoring-savefile /data/output/detection-evaluation/height-scoring.png \
            --predicted-attribute-savefile /data/output/detection-evaluation/height-scoring-matched-values.csv
    ```

    Windows:

    ```powershell
    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest `
        python -m tree_registration_and_matching.entrypoints.score_detected_trees `
            /data/ground-reference/ofo-ground-reference-trees_0030.gpkg `
            /data/detected-trees/composite1_tree-tops_geometric_v01.gpkg `
            /data/ground-reference/ofo-ground-reference-plot_0030.gpkg `
            --shift-file /data/registration/reference-drone-registration.csv `
            --field-attribute-to-score height `
            --drone-attribute-to-score height `
            --continuous-scoring-attribute `
            --scoring-metrics-savefile /data/output/detection-evaluation/height-scoring-metrics.json `
            --vis-attribute-scoring-savefile /data/output/detection-evaluation/height-scoring.png `
            --predicted-attribute-savefile /data/output/detection-evaluation/height-scoring-matched-values.csv
    ```

=== "Python command-line entrypoint"

    In your terminal, activate the `tree-registration-and-matching` Conda environment.

    ```bash
    conda activate tree-registration-and-matching
    ```

    Then run the [tree detection scoring entrypoint script](https://github.com/open-forest-observatory/tree-registration-and-matching/blob/main/tree_registration_and_matching/entrypoints/score_detected_trees.py).

    ```bash
    python -m tree_registration_and_matching.entrypoints.score_detected_trees \
        ${DATA_DIR}/ground-reference/ofo-ground-reference-trees_0030.gpkg \
        ${DATA_DIR}/detected-trees/composite1_tree-tops_geometric_v01.gpkg \
        ${DATA_DIR}/ground-reference/ofo-ground-reference-plot_0030.gpkg \
        --shift-file ${DATA_DIR}/registration/reference-drone-registration.csv \
        --field-attribute-to-score height \
        --drone-attribute-to-score height \
        --continuous-scoring-attribute \
        --scoring-metrics-savefile ${DATA_DIR}/output/detection-evaluation/height-scoring-metrics.json \
        --vis-attribute-scoring-savefile ${DATA_DIR}/output/detection-evaluation/height-scoring.png \
        --predicted-attribute-savefile ${DATA_DIR}/output/detection-evaluation/height-scoring-matched-values.csv
    ```

=== "Python script"

    Run the following code from within the `tree-registration-and-matching` Conda environment.

    ```python
    from pathlib import Path

    from tree_registration_and_matching.entrypoints.score_detected_trees import (
        score_detected_trees,
    )

    # Change this line
    DATA_DIR = Path("path/to/data")

    # Define the inputs
    FIELD_TREES_FILE = Path(
        DATA_DIR, "ground-reference", "ofo-ground-reference-trees_0030.gpkg"
    )
    DRONE_TREES_FILE = Path(
        DATA_DIR, "detected-trees", "composite1_tree-tops_geometric_v01.gpkg"
    )
    FIELD_PLOT_BOUNDS_FILE = Path(
        DATA_DIR, "ground-reference", "ofo-ground-reference-plot_0030.gpkg"
    )
    SHIFT_FILE = Path(DATA_DIR, "registration", "reference-drone-registration.csv")
    FIELD_ATTRIBUTE_TO_SCORE = "height"
    DRONE_ATTRIBUTE_TO_SCORE = "height"
    CATEGORICAL_SCORING_ATTRIBUTE = False

    # Define the outputs
    SCORING_METRICS_SAVEFILE = Path(
        DATA_DIR, "output", "detection-evaluation", "height-scoring-metrics.json"
    )
    VIS_ATTRIBUTE_SCORING_SAVEFILE = Path(
        DATA_DIR, "output", "detection-evaluation", "height-scoring.png"
    )
    PREDICTED_ATTRIBUTE_SAVEFILE = Path(
        DATA_DIR, "output", "detection-evaluation", "height-scoring-matched-values.csv"
    )


    _, metrics = score_detected_trees(
        field_trees_file=FIELD_TREES_FILE,
        drone_trees_file=DRONE_TREES_FILE,
        field_plot_bounds_file=FIELD_PLOT_BOUNDS_FILE,
        shift_file=SHIFT_FILE,
        field_attribute_to_score=FIELD_ATTRIBUTE_TO_SCORE,
        drone_attribute_to_score=DRONE_ATTRIBUTE_TO_SCORE,
        categorical_scoring_attribute=CATEGORICAL_SCORING_ATTRIBUTE,
        scoring_metrics_savefile=SCORING_METRICS_SAVEFILE,
        vis_attribute_scoring_savefile=VIS_ATTRIBUTE_SCORING_SAVEFILE,
        predicted_attribute_savefile=PREDICTED_ATTRIBUTE_SAVEFILE,
    )
    print(metrics)
    ```

The same approach can be used to score a categorical attribute such as species as shown below. This produces a confusion matrix visualization and class-wise and overall precision, recall, and F1 metric values. Note that the classified tree tops are used as input.

![scoring species prediction](/assets/images/tutorials/composite1_species_scoring.png)

=== "Docker"

    Linux/Mac:

    ```bash
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_DIR}:/data" \
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest \
        python -m tree_registration_and_matching.entrypoints.score_detected_trees \
            /data/ground-reference/ofo-ground-reference-trees_0030.gpkg \
            /data/classified-trees/composite1_tree-tops_geometric_v01_species.gpkg \
            /data/ground-reference/ofo-ground-reference-plot_0030.gpkg \
            --shift-file /data/registration/reference-drone-registration.csv \
            --field-attribute-to-score species_code \
            --drone-attribute-to-score species \
            --categorical-scoring-attribute \
            --scoring-metrics-savefile /data/output/detection-evaluation/species-scoring-metrics.json \
            --vis-attribute-scoring-savefile /data/output/detection-evaluation/species-scoring.png \
            --predicted-attribute-savefile /data/output/detection-evaluation/species-scoring-matched-values.csv
    ```

    Windows:

    ```powershell
    docker run --rm `
        -v "${env:DATA_DIR}:/data" `
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest `
        python -m tree_registration_and_matching.entrypoints.score_detected_trees `
            /data/ground-reference/ofo-ground-reference-trees_0030.gpkg `
            /data/classified-trees/composite1_tree-tops_geometric_v01_species.gpkg `
            /data/ground-reference/ofo-ground-reference-plot_0030.gpkg `
            --shift-file /data/registration/reference-drone-registration.csv `
            --field-attribute-to-score species_code `
            --drone-attribute-to-score species `
            --categorical-scoring-attribute `
            --scoring-metrics-savefile /data/output/detection-evaluation/species-scoring-metrics.json `
            --vis-attribute-scoring-savefile /data/output/detection-evaluation/species-scoring.png `
            --predicted-attribute-savefile /data/output/detection-evaluation/species-scoring-matched-values.csv
    ```

=== "Python command-line entrypoint"

    In your terminal, activate the `tree-registration-and-matching` Conda environment.

    ```bash
    conda activate tree-registration-and-matching
    ```

    Then run the [tree detection scoring entrypoint script](https://github.com/open-forest-observatory/tree-registration-and-matching/blob/main/tree_registration_and_matching/entrypoints/score_detected_trees.py).

    ```bash
    python -m tree_registration_and_matching.entrypoints.score_detected_trees \
        ${DATA_DIR}/ground-reference/ofo-ground-reference-trees_0030.gpkg \
        ${DATA_DIR}/classified-trees/composite1_tree-tops_geometric_v01_species.gpkg \
        ${DATA_DIR}/ground-reference/ofo-ground-reference-plot_0030.gpkg \
        --shift-file ${DATA_DIR}/registration/reference-drone-registration.csv \
        --field-attribute-to-score species_code \
        --drone-attribute-to-score species \
        --categorical-scoring-attribute \
        --scoring-metrics-savefile ${DATA_DIR}/output/detection-evaluation/species-scoring-metrics.json \
        --vis-attribute-scoring-savefile ${DATA_DIR}/output/detection-evaluation/species-scoring.png \
        --predicted-attribute-savefile ${DATA_DIR}/output/detection-evaluation/species-scoring-matched-values.csv
    ```

=== "Python script"

    Run the following code from within the `tree-registration-and-matching` Conda environment.

    ```python
    from pathlib import Path

    from tree_registration_and_matching.entrypoints.score_detected_trees import (
        score_detected_trees,
    )

    # Change this line
    DATA_DIR = Path("path/to/data")

    # Define the inputs
    FIELD_TREES_FILE = Path(
        DATA_DIR, "ground-reference", "ofo-ground-reference-trees_0030.gpkg"
    )
    DRONE_TREES_FILE = Path(
        DATA_DIR,
        "classified-trees",
        "composite1_tree-tops_geometric_v01_species.gpkg",
    )
    FIELD_PLOT_BOUNDS_FILE = Path(
        DATA_DIR, "ground-reference", "ofo-ground-reference-plot_0030.gpkg"
    )
    SHIFT_FILE = Path(DATA_DIR, "registration", "reference-drone-registration.csv")
    FIELD_ATTRIBUTE_TO_SCORE = "species_code"
    DRONE_ATTRIBUTE_TO_SCORE = "species"
    CATEGORICAL_SCORING_ATTRIBUTE = True

    # Define the outputs
    SCORING_METRICS_SAVEFILE = Path(
        DATA_DIR, "output", "detection-evaluation", "species-scoring-metrics.json"
    )
    VIS_ATTRIBUTE_SCORING_SAVEFILE = Path(
        DATA_DIR, "output", "detection-evaluation", "species-scoring.png"
    )
    PREDICTED_ATTRIBUTE_SAVEFILE = Path(
        DATA_DIR,
        "output",
        "detection-evaluation",
        "species-scoring-matched-values.csv",
    )

    _, metrics = score_detected_trees(
        field_trees_file=FIELD_TREES_FILE,
        drone_trees_file=DRONE_TREES_FILE,
        field_plot_bounds_file=FIELD_PLOT_BOUNDS_FILE,
        shift_file=SHIFT_FILE,
        field_attribute_to_score=FIELD_ATTRIBUTE_TO_SCORE,
        drone_attribute_to_score=DRONE_ATTRIBUTE_TO_SCORE,
        categorical_scoring_attribute=CATEGORICAL_SCORING_ATTRIBUTE,
        scoring_metrics_savefile=SCORING_METRICS_SAVEFILE,
        vis_attribute_scoring_savefile=VIS_ATTRIBUTE_SCORING_SAVEFILE,
        predicted_attribute_savefile=PREDICTED_ATTRIBUTE_SAVEFILE,
    )
    print(metrics)
    ```