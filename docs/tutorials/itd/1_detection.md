---
weight: 20
---

# Task 1: Detection & mapping

We will use the OFO's [Tree Detection Framework](https://github.com/open-forest-observatory/tree-detection-framework) to detect and delineate tree crowns from drone-derived data products using a variety of approaches, including a geometric algorithm applied to a [canopy height model] (CHM) and several different computer vision algorithms applied an [orthomosaic].

## Input data

| Name                | Source                         | Example file                                                             |
| ------------------- | ------------------------------ | ------------------------------------------------------------------------ |
| [Canopy height model] | Photogrammetry post-processing | TODO: Thumbnail [000452-subset_chm.tif](TODO: Link to Box)               |
| [Orthomosaic]         | Photogrammetry post-processing | TODO: Thumbnail [000452-subset_ortho-chm-ptcloud.tif](TODO: Link to Box) |

## Setup

=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

=== "Native Python"

    TODO: Pointer to TDF installation instructions.

Download the input data to your computer. We recommend downloading the entire [tutorial data folder](TODO: Link to Box), which contains the data for all OFO tutorials, but you can also download just the input data needed for this task, listed above. {TODO: Will we just repeat this blurb on every tutorial task page? Better way to do this?}

## Geometric tree detection from a canopy height model

First, we will use a *geometric algorithm* implemented in the Tree Detection Framework to detect treetops as local maxima in the canopy height model (CHM). This approach uses a [variable-radius local maximum filter].

TODO: More context?

=== "Docker (recommended)"

    ```bash
    # TODO: Docker command
    ```

=== "Native Python"

    TODO: Do we use the python entrypoint script? Or load objects and call functions directly? Or somehow reference a notebook? I'd opt to avoid a notebook as the main reference, but perhaps we can link to a notebook at the end as an alternative option.

    ```python
    # TODO: First python line
    # TODO: Second python line
    ```



## Computer vision tree detection from an orthomosaic

TODO: Finish
