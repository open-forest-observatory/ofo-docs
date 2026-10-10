<!-- 
=== Podman

TODO: Derek's notes below

Run as administrator in PowerShell:

`winget install RedHat.Podman`

Then in a normal PowerShell:

``` powershell
podman machine init
podman machine set --rootful
```
 -->


<!-- 
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
-->


