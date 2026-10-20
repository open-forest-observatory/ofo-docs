---
weight: 20
---

# Task 1: Co-registration

Before comparing predicted trees against ground reference data, we need to make sure the two datasets are spatially co-registered. While both the drone imagery and reference tree locations are georeferenced with GPS, each set of measurements can have an independent bias due to atmospheric effects. This creates a spatial offset which is commonly on the order of several meters between the two sets of data.


## Required input data

| Name                  | Source                         | Example file                                                                                   |
| --------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------- |
| [Canopy height model] | Photogrammetry post-processing | [composite1_chm-mesh.tif](https://ucdavis.box.com/s/s02rs8rndobua45ukw0rjb8zysihicl4)          |
| Ground reference trees | Manual field work | [ofo-ground-reference-trees_0030.gpkg](https://ucdavis.box.com/s/4z4j3npqbdwx2p24mv2zriw3zm1xlfbn)          |

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

To align the drone and reference data we use an algorithm that takes the [CHM] linked above and reference tree locations and heights as input. Specifically, we compute the correlations between the height of the reference trees and the location on the CHM at which the trees are, across a grid of shifts from the initial location. The shift which maximizes the correlation between observed and CHM-derived height is considered the optimal registration.


=== "Docker"

    Linux/Mac:

    ```bash
    export DATA_FOLDER="/ofo-share/repos/david/ofo-docs/data"
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "${DATA_FOLDER}:/data" \
        ghcr.io/open-forest-observatory/tree-registration-and-matching:latest \
        python -m tree_registration_and_matching.entrypoints.register_trees_to_CHM \
            --CHM-file /data/inputs/drone/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
            --tree-points-file /data/inputs/ground-reference/ofo-ground-reference-trees_0030.gpkg \
            --output-shift-summary /data/intermediate/reference-drone-registration.csv

    ```

    Windows: TODO

    ```powershell
    ```

=== "Jupyter"

    This step is performed by lines XX-YY (TODO) of the Jupyter notebook {TODO: Link to notebook}.

=== "Python command-line entrypoint"

    ```bash
    ```

=== "Python script"

    ```python
    # TODO write out the appropriate parts of the entrypoint here:
    # https://github.com/open-forest-observatory/tree-registration-and-matching/blob/4246c5185833061989c91314eddec71d28cafb19/tree_registration_and_matching/entrypoints/match_field_attributes_to_drone.py#L15
    ```