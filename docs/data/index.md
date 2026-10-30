---
weight: 2
---

# OFO Datasets

The Open Forest Observatory (OFO) Open Data Catalog consists of two main components: (1) ground-based manual forest inventory plot data and (2) drone imagery and derived data (e.g. orthomosaics, canopy height models, and maps of automatically detected trees). Many of the ground plots are covered by one or more drone collects, facilitating development and validation of drone-based forest mapping methods.

## Web-based data catalog

You can easily browse, preview, and download OFO drone-derived data and ground reference data via the [OFO Data Catalog](https://openforestobservatory.org/data/). Be sure to read the [Important details and considerations](#important-details-considerations-and-usage-restrictions) section below to understand important usage restrictions and determine what datasets are appropriate to use in your work.

## Bulk/programmatic data access

Be sure to read the [Important details and considerations](#important-details-and-considerations-and-usage-restrictions) section below to understand important usage restrictions and determine what datasets are appropriate to use in your work.

### Ground reference data

The ground reference dataset consists of traditional manual forest inventory plot data. These data files represent the locations and characteristics of trees in plots that are mapped by technicians on the ground using traditional forest tree stem-mapping methods.

- `ofo_ground-reference_plots.gpkg`: Plot-level data and metadata, including plot geospatial footprint, survey dates, protocol components such as tally tree definitions, and data license, in geospatial (geopackage) format
    - `ofo_ground-reference_plots_metadata.md`: Metadata describing the plot dataset, including column definitions, in markdown format.
- `ofo_ground-reference_trees.gpkg`: Tree-level data, including tree stem geospatial location, species, size, in geospatial (geopackage) format
    - `ofo_ground-reference_trees_metadata.md`: Metadata describing the tree dataset, including column definitions, in markdown format.

The [OFO web catalog](https://openforestobservatory.org/data/drone/) contains web preview functionality for ground reference plot data.

### Drone-derived data

- `ofo_drone-missions.gpkg` Mission-level data and metadata, including geospatial footprint, flight altitude, raw image density, and data license, in geospatial (geopackage) format
    - `ofo_drone-missions_metadata.md`: Metadata describing the drone missions dataset, including column definitions, in markdown format.

Data files themselves are accessible via the Jetstream2 Object Store (S3-compatible bucket):

- Public HTTP URL template for orthomosaics (cloud-optimized geotiff): `https://js2.jetstream-cloud.org:8001/ofo-public/drone/missions_03/<mission-id>/photogrammetry_03/full/<mission-id>_ortho-dsm-ptcloud.tif`
- Many other data products (e.g., canopy height model, raw images) and previews/thumbnails are also available (see 'Data types', below. A representative (but truncated) bucket file listing illustrating file naming conventions can be obtained at: <https://js2.jetstream-cloud.org:8001/swift/v1/ofo-public/>

The data files are also accessible via S3 protocol (e.g. AWS S3 CLI, rclone, CyberDuck) at endpoint: <https://js2.jetstream-cloud.org:8001/>, bucket ofo-public.

The [OFO web catalog](https://openforestobservatory.org/data/drone/) contains web preview and direct download functionality for drone-derived data.

The [OFO STAC catalog](https://github.com/open-forest-observatory/stac) is an alternative means of data access via the standard Spatio-Temporal Asset Catalog specification, but it currently reflects an older processing run for a subset of missions. We plan to update it to reflect our current catalog by the end of 2026 and will prioritize this if/when requested by an external user.

#### Drone-derived data types

- Geospatial orthomosaics are named `<mission-id>_ortho-dsm-ptcloud.tif` or `<mission-id>_ortho-dsm-mesh.tif` depending whether they were based on a digital surface model made from the point cloud (more detailed) or the mesh (smoother).
- Canopy height models are named `<mission-id>_chm-ptcloud.tif` or `<mission-id>_chm-mesh.tif` depending whether they were based on a digital surface model made from the point cloud (more detailed) or the mesh (smoother). All CHMs use the point cloud-derived DTM as their terrain model.
- The digital terrain model is made from the point cloud (only) and is named `<mission-id>_dtm-ptcloud.tif`.
- Each processed product should also have a color point cloud (3D), mesh model (3D) (filename contains "model"; both in an arbitrary project-specific coordinate system, or a global geospatial coordinate system), digital surface models (from mesh and point cloud), raw photo geospatial locations, camera poses, and processing report. The mapping of these data types to the files should be clear based on the filenames.
- Most missions also have detected treetops and crowns (the latter from each of two algorithms, Silva and Watershed). They are located in the `itd-0001` folder beneath the mission's `photogrammetry_03` folder.
- You can stream the point cloud into the Entwine viewer by going to Entwine selecting "Add data" and entering the HTTP URL of the point cloud, such as: [https://js2.jetstream-cloud.org:8001/ofo-public/drone/missions_01/000001/photogrammetry_03//full/000001_points-copc.laz](https://js2.jetstream-cloud.org:8001/ofo-public/drone/missions_01/000001/processed_02/full/000001_points-copc.laz)

## Important details, considerations, and usage restrictions

**It is essential that you read these details before using the data.**

The OFO data catalog is a compilation of contributions from many organizations and individuals. Each data item (e.g. ground-based manual inventory plot; drone collect and derived products) has its own Creative Commons data license, as indicated by the `license` attribute (column) in the associated data/metadata file(s) (see below).

Use of any data to produce any derivative products (or simply re-sharing the data as-is) requires (1) attribution to the data contributors (not the OFO) and specification of a data license equivalent to or compatible with the original data license, (2) acknowledgment of the Open Forest Observatory as the means used to discover and access the data, (3) inclusion of any metadata necessary for others to understand and use any OFO-derived data included in the derived data product, and (4) any other requirements specified in the license(s) of the datasets you use.

For questions around the use and interpretation of the data, contact openforestobservatory@ucdavis.edu.

### Overall considerations

- The metadata markdown files linked above are critical to read carefully, as they describe data attributes that could affect whether to include or exclude some plots depending on the analysis. For example, different plots used different minimum tree size thresholds for inclusion, and some plots consist of nested circles in which trees of different sizes were measured (large plot for large trees, small plot for small trees). Similarly, different drone missions used different flight altitudes and image overlaps.
- **Important usage restriction:** We have designated a stratified subset of approximately 20% of plots and drone missions to be excluded from training ML models that are intended for use by the forest mapping/ML community. For such applications, these datasets are reserved for use as test data for model evaluation and intercomparison. The plots to be excluded from training are indicated in the data/metadata records by the value `true` in the column `withhold_from_training`.
- Data license varies by dataset. All use Creative Commons licenses (most of them requiring data contributor attribution in derivative products), but please be aware that some plot data licenses include non-commercial and share-alike clauses that limit derivative works and their uses in certain contexts.
- The mapping of drone missions to ground reference plots is not 1:1. Some ground plots are covered by multiple drone missions (or zero drone missions) and vice-versa.
- Ground reference plots are not necessarily spatially co-registered to the drone missions that include them. In most/all cases, they should be within ~10 m, but for most comparison analysis, it will likely be necessary to perform (manual or automated) co-registration to optimally align the ground data to the drone data.

### Ground-reference data considerations

- Survey protocol varies by plot. Protocols differ in many attributes, including what tree size attributes are measured (e.g., DBH, height, both), what trees are surveyed vs. ignored, etc. The protocol definition for a given plot is documented in plot-level data attributes.
- Many OFO drone inventories consist of two missions: (1) high-altitude, nadir imaging and (2) low-altitude, oblique imaging. The latter is intended to complement the former and allow for enhanced multi-view tree detection and species classification from raw drone images. For applications that do not involve interpretation of raw drone images, the oblique missions should likely be excluded.

## Representative datasets

### Emerald Point

This is a relatively flat mixed-conifer stand on a peninsula on the shore of Lake Tahoe, California. It contains a large (> 3 ha) field based tree map with detailed tree-level attributes. The drone imagery and field reference data linked here were the basis for the [paper by Young et al. (2022)](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13860).

#### Over-canopy drone imagery

The drone imagery datasets linked here have a very high image density. For a more standard image density dataset, see "Emerald Point subset", below.

[120 m nadir](https://openforestobservatory.org/data/drone/mission-details/000434/)

[90 m oblique (25 deg)](https://openforestobservatory.org/data/drone/mission-details/000440/)

#### Field reference data

[Visualization](https://openforestobservatory.org/data/ground-ref/plot-details/0068/)
Please note the data licensing details on the visualization page, which apply to the data access link below.

[Data access](https://ucdavis.box.com/s/56qrdofabfr69tyc5aqmyrjta11a829t). Data also available via the plots and trees data files linked above.

### Emerald Point subset

This is the same site as above, but it is a smaller footprint with sparser images (a cropped and thinned version of the above) for faster processing time.

#### Over-canopy drone imagery

[120 m nadir](https://ucdavis.box.com/s/qg1nw8pw64zpua13jiv8l36gk502xhtd)

#### Field reference data

This drone dataset footprint covers the same field reference dataset linked above.


### Stanislaus-Tuolumne Experimental Forest - OFO field plot 0077

#### Over-canopy drone imagery

[120 m nadir](https://openforestobservatory.org/data/drone/mission-details/000810/)

[80 m oblique (35 deg)](https://openforestobservatory.org/data/drone/mission-details/000808/)

#### Under-canopy imagery

This imagery was collected by walking a serpentine ("lawnmower") pattern in a portion of the stand with a GoPro on a 2 m pole set to record one 360 degree spherical image every 2 seconds.

[Understory 360 degree images](https://ucdavis.box.com/s/3c41u8qwdkoz0ju331p9s2dinpsi1htd)

#### Field reference data

[Visualization](https://openforestobservatory.org/data/ground-ref/plot-details/0077/)

Data available via the plots and trees data files linked above.


### Stanislaus-Tuolumne Experimental Forest - OFO field plot 0079

#### Drone imagery

[120 m nadir (same as previous stand)](https://openforestobservatory.org/data/drone/mission-details/000810/)

[80 m oblique (35 deg) (same as previous stand)](https://openforestobservatory.org/data/drone/mission-details/000808/)

#### Under-canopy imagery

This imagery was collected by walking a serpentine ("lawnmower") pattern in a portion of the stand with a GoPro on a 2 m pole set to record one 360 degree spherical image every 2 seconds.

[Understory 360 degree images](https://ucdavis.box.com/s/jdk4i783n3ngjfi2bg8atacapqvj7cqp)

#### Ground reference data

[Visualization](https://openforestobservatory.org/data/ground-ref/plot-details/0079/)

Data available via the plots and trees data files linked above.


### UC Berkeley Blodgett Experimental Forest - OFO field plot 0117

#### Over-canopy drone imagery

[120 m nadir](https://openforestobservatory.org/data/drone/mission-details/000649/)

[80 m oblique (35 deg)](https://openforestobservatory.org/data/drone/mission-details/000650/)

#### Under-canopy imagery

This imagery was collected by walking a serpentine ("lawnmower") pattern in a portion of the stand with a GoPro on a 2 m pole set to record one 360 degree spherical image every 2 seconds.

[Understory 360 degree images](https://ucdavis.box.com/s/xoml4h9wpu68iqxube0hsv1bna604wj3)

#### Ground reference data

[Visualization](https://openforestobservatory.org/data/ground-ref/plot-details/0117/)

Data available via the plots and trees data files linked above.
