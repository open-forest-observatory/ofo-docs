---
weight: 20
---

# Task 2: Evaluation

The final task is assessing the quality of the detected trees. This is done by comparing the locations of detected trees to those of spatially-shifted field reference trees. This process produces precision, recall, and F1 scores for the tree detection task.

## Required input data

| Name                  | Source                         | Example file                                                                                   |
| --------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------- |
| Shifted reference trees | Registration algorithm       | [ofo-ground-reference-trees_0030_shifted.gpkg](TODO)          |
| Detected trees        | Tree detection algorithm       | [composite1_tree-tops_geometric_v01.gpkg](TODO)          |

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

TODO

=== "Docker"

    Linux/Mac:

    ```bash
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_FOLDER}:/data" \
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest \
    ```

    Windows: TODO

    ```powershell
    ```

=== "Jupyter"

    This step is performed by lines XX-YY (TODO) of the Jupyter notebook {TODO: Link to notebook}.

=== "Python command-line entrypoint"

    ```bash
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"
    ```

=== "Python script"

    ```python
    # TODO write out the appropriate parts of the entrypoint here:
    # https://github.com/open-forest-observatory/tree-registration-and-matching/blob/4246c5185833061989c91314eddec71d28cafb19/tree_registration_and_matching/entrypoints/match_field_attributes_to_drone.py#L15
    ```