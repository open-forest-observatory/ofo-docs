---
weight: 20
---

# Task 1: Detection & mapping

We will use the OFO's [Tree Detection Framework](https://github.com/open-forest-observatory/tree-detection-framework) to detect and delineate tree crowns from drone-derived data products using a variety of approaches, including a geometric algorithm applied to a [canopy height model] (CHM) and several different computer vision algorithms applied an [orthomosaic].

## Required input data

| Name                | Source                         | Example file                                                             |
| ------------------- | ------------------------------ | ------------------------------------------------------------------------ |
| [Canopy height model] | Photogrammetry post-processing | [000452-subset_chm.tif](TODO: Link to Box)               |
| [Orthomosaic]         | Photogrammetry post-processing | [000452-subset_ortho-chm-ptcloud.tif](TODO: Link to Box) |

## Setup

=== "Docker (recommended)"

    Follow our [Docker guide](/tutorials/index.md#docker) to understand what Docker is and ensure your system is set up to run Docker containers.

=== "Native Python"

    TODO: Pointer to TDF installation instructions.

Download the input data to your computer. We recommend downloading the entire [tutorial data folder](TODO: Link to Box), which contains the data for all OFO tutorials, but you can also download just the input data needed for this task, listed above. {TODO: Will we just repeat this blurb on every tutorial task page? Better way to do this?}

## Geometric tree detection from a canopy height model

First, we will use a *geometric algorithm* implemented in the Tree Detection Framework to detect treetops as local maxima in the canopy height model (CHM). This approach uses a [variable-radius local maximum filter]. We will demonstrate with the CHM linked above:

![CHM](/assets/images/tutorials/composite1_chm-mesh.png)

TODO: More context?

=== "Docker (recommended)"

    Linux/Mac:

    ```bash
    docker run --rm --user "$(id -u):$(id -g)" \
        -v "$HOME/ofo-tutorial-testing:/data" \
        ghcr.io/open-forest-observatory/tree-detection-framework:latest \
        python -m tree_detection_framework.entrypoints.detect_geometric_two_stage \
            /data/inputs/photogrammetry-postprocessed/full/composite1_chm-mesh.tif \
            /data/outputs/detected-trees/composite1_tree-tops_v02.gpkg \
            --tree-crowns-save-path /data/outputs/detected-trees/composite1_tree-crowns_v02.gpkg \
            --raster-blur-sigma 0.5 \
            --tree-top-detector-kwargs '{"a": 0, "b": 0.0325, "c": 0.25, "min_ht": 5}'
    ```

    Windows:

    ```powershell
    # TODO: PowerShell Docker command
    ```

=== "Podman (Windows)"

    TODO: This worked, though it took a long time to download the container blobs. Derek is attempting to provide this as an alternative to Docker Desktop for Windows user, which is commercial software requiring a paid license for members of organizations larger than 250. But that might be exempted for using non-commercial open-source software like the OFO containers (hard to tell from license).

    ```powershell
    podman machine start
    podman --connection podman-machine-default-root run --rm `
    -v "$HOME\Documents\ofo-tutorial-testing:/data" `
    ghcr.io/open-forest-observatory/tree-detection-framework:latest `
    python -m tree_detection_framework.entrypoints.detect_geometric_two_stage `
        /data/inputs/photogrammetry-postprocessed/full/composite1_chm-mesh.tif `
        /data/outputs/detected-trees/composite1_tree-tops_v01.gpkg `
        --tree-crowns-save-path /data/outputs/detected-trees/composite1_tree-crowns_v01.gpkg `
        --raster-blur-sigma 0.5 `
        --tree-top-detector-kwargs '{"a": 0, "b": 0.0325, "c": 0.25, "min_ht": 5}'
    ```    


=== "Native Python"

    TODO: Do we use the python entrypoint script? Or load objects and call functions directly? Maybe both (as separate taps)? Somehow reference a notebook? I'd opt to avoid a notebook as the main reference, but perhaps we can link to a notebook at the end as an alternative option.

    ```python
    # TODO: First python line
    # TODO: Second python line
    ```

This command saves two geospatial output files: points representing detected tree tops and polygons representing detected tree crowns. You can visualize these outputs in a GIS software like [QGIS](https://qgis.org/en/site/):

![CHM with detected trees](/assets/images/tutorials/composite1_chm-mesh_w-detections_v01.png)

The geometric tree detection algorithm can be parameterized in many different ways. For example, the value passed to `--raster-blur-sigma` controls the amount of smoothing applied to the CHM before detecting local maxima. The values given for `a`, `b`, and `c` in the `--tree-top-detector-kwargs` affects the local maximum search radius relative to the height of the tree. Other parameters not supplied here (and thus using their defaults) include `chip_size` and `chip_stride`, which control how large CHMs are split up into manageable chunks prior to processing, and `resolution`, which controls the resolution the CHM is resampled to prior to running the algorithm. See the [Tree Detection Framework documentation](https://open-forest-observatory.github.io/tree-detection-framework/command_line_usage/detect_geometric_two_stage/) for a detailed description of all parameters. Here is an example of the effect of setting the treetop detector parameter `c` to `5`.

![CHM with detected trees](/assets/images/tutorials/composite1_chm-mesh_w-detections_v02.png)

## Computer vision tree detection from an orthomosaic

TODO: Finish
