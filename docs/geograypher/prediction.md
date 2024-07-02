# Prediction tasks with Geograypher

[Geograypher](https://github.com/open-forest-observatory/geograypher) is used for making predictions about a landscape using multi-view drone data along with field reference surveys.

## Workflow

The common workflow I've used is as follows.

### Photogrammetry

Geograypher requires that the drone survey data is pre-processed using photogrammetry. This processing can be done graphically using `Agisoft Metashape` or can be scripted with [automate-metashape](https://github.com/open-forest-observatory/automate-metashape). For tasks using the raw images, the camera poses and mesh must be provided. A DTM is optional, but helpful in many applications for identifying the ground points. For the workflows using the orthomosaic, it is the only product that is required.

### Standardizing field reference data

Geograypher expects that the field reference data will be standardized before it can be used. Currently, this means that the data should be in a geospatial format that can be read by `geopandas`, has a `Polygon/MultiPolygon` geometry, and a has single column that contains the label you want to predict. For example, in a species classification problem, the user could provide a file with one `MultiPolygon` per species, with a column called `species` identifying what species each region corresponds to. Alternatively, they could provide `Polygon` data per tree, with one entry per tree, and a column called `species` identifying what species each tree is.

Standardizing the field reference data can take many forms, but it problem-specific and can usually be accomplished with standard geospatial tools, either graphical ones such as `QGIS` or scripts relying on libraries such `geopandas`. Precise geo-referencing relative to the photogrammetry products is critical, and this may required manual alignment using a graphical tool or scripted corrections based on RTK measurements. The format of the data may not exactly match the required specification. For example, `Point` data with an associated `radius` should be transformed into a `Polygon`-typed circle. Often the label you want to classify is not directly present in the raw field reference data. For example, if you want to both classify species and whether it is alive or dead, you may have to concatenate the information from the two columns to provide a unique label for each situation. Alternatively, you may want to merge labels before prediction, drop a subset of them, or override some labels using another column. All of these operations are easy to do using `geopandas`, and presumably possible in other tools.

### Creating training data

Geograypher can process the data from the first two steps and produce a folder of labels that can be used for training. These workflows are implemented in [`render_mesh.py`](https://github.com/open-forest-observatory/multiview-mapping-toolkit/blob/main/multiview_mapping_toolkit/entrypoints/render_mesh.py) and [`render_labels.ipynb`](https://github.com/open-forest-observatory/multiview-mapping-toolkit/blob/main/examples/render_labels.ipynb) for the image-based workflows and [`orthomosaic_predictions.py`](https://github.com/open-forest-observatory/multiview-mapping-toolkit/blob/main/multiview_mapping_toolkit/entrypoints/orthomosaic_predictions.py) for orthomosiacs. For more information see the command line arguments of these files.

### Training models

Once the training labels have been exported, the user is free to train any sort of prediction model on them using their own frameworks. The Geograypher project aims to produce training data and consume predictions, but is agnostic to what happens in between.

OFO currently supports a workflow for making semantic segmentation predictions using the [`mmsegmentation`](https://github.com/open-mmlab/mmsegmentation) framework. This open-source project built on `PyTorch` provides a standardized way to use a wide array of state-of-the-art semantic segmentation models interchangeably. To process the data into the required training format, you can use [`segmentation_utils`](https://github.com/open-forest-observatory/segmentation_utils). Specifically, [`remap_classes.py`](https://github.com/open-forest-observatory/segmentation_utils/blob/main/dev/dataset_creation/remap_classes.py) can be used to merge or relabel classes, and [`folder_to_cityscapes.py`](https://github.com/open-forest-observatory/segmentation_utils/blob/main/dev/dataset_creation/folder_to_cityscapes.py) can be used to process a folder of labels into the required format. By default, this creates a config file that allows you to train a [Segformer](https://github.com/open-mmlab/mmsegmentation/tree/main/configs/segformer) model on this data. This code can be run using the `mmseg-utils` conda environment.

You can train a model using [`mmseg/tools/train.py`](https://github.com/open-mmlab/mmsegmentation/blob/main/tools/train.py). Simply point the script at the config file generated in the last step. This can be run using the `openmmlab` conda environment.

## Generating predictions

As discussed before, you can generated predictions from a ML model using whatever framework you want. If you want to use the model trained with `mmsegmentation` in the last step, you can use the [`tools/inference.py`](https://github.com/open-forest-observatory/mmsegmentation/blob/dr/tile-inference/tools/inference.py) script in our fork of `mmsegmentation`. Point this at the trained model and the folder of images you want to generated predictions on. This will generated a folder of predictions structured the same way as the input data.

You can visualize the predictions using [`segmentation_utils visualize_semantic_labels.py`](https://github.com/open-forest-observatory/segmentation_utils/blob/main/dev/visualization/visualize_semantic_labels.py).

## Aggregating predictions

You can use [`aggregate_viewpoints.py`](https://github.com/open-forest-observatory/multiview-mapping-toolkit/blob/main/multiview_mapping_toolkit/entrypoints/aggregate_viewpoints.py) or [`aggregate_predictions.ipynb`](https://github.com/open-forest-observatory/multiview-mapping-toolkit/blob/main/examples/aggregate_predictions.ipynb) to aggregate the predictions together into geo-spatial coordinates. If you want to do further analysis, you should export the predictions into a geofile.

## Evaluating predictions
