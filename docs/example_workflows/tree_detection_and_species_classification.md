---
title: Tree Detection and Species Classification
weight: 100
---

Data to reproduce all steps of these experiments can be found [here](https://broken/link).

Fly the drone survey using these parameters

Process the images with `automate-metashape`. This aligns the images to produce several different types of data.

Detect trees with `ofo-R`. This is done by computing a canopy height model and then detecting local maxima.

Link the detected trees to field-based observations using `OFO-R`. This is done with algorithm developed for this task.

Using `geograypher`, render per-image training labels using the field reference data