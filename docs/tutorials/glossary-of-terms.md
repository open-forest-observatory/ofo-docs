---
weight: 100
# To make a term linkable from any page by writing it in square brackets, add
# it (and any variants, e.g. plurals) to includes/glossary-links.md, pointing
# to its heading anchor.
---

# Glossary of terms

This page defines common technical terms used in the OFO tutorials.

## Canopy height model (CHM) { #chm }

A raster data product that represents the height of vegetation above the ground surface. It is a geospatial data product, allowing for precise measurements and analysis using GIS tools.

![Canopy height model](/assets/images/tutorials/composite1_chm-mesh.png)

## Orthomosaic { #orthomosaic }

A georeferenced image created by stitching together multiple overlapping aerial photographs. It is a geospatial data product, allowing for precise measurements and analysis using GIS tools.

![Orthomosaic](/assets/images/tutorials/composite1_ortho-dsm-ptcloud.png)

## Digital terrain model (DTM) { #dtm }

A representation of the bare-earth altitude. This is produced by photogrammetry which employs algorithms to identify which portion of the scene represents ground. In the visualization below, brightness represents altitude, normalized to min and max.

![DTM](/assets/images/tutorials/composite1_dtm.png)

## Mesh model { #mesh-model }

A representation of a surface in 3D produced by many photogrammetry tools. It consists of a set of points called vertices connected by triangular faces. This data structure is common in the field of computer graphics and is used to perform rendering operations.

![Mesh model](/assets/images/tutorials/mesh-model-illustration.png)

<div class="sketchfab-embed-wrapper"> <iframe title="OFO North Yuba Stand 1" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/530e3b7b1dd54b8b951f4c72d5c6901b/embed"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/ofo-north-yuba-stand-1-530e3b7b1dd54b8b951f4c72d5c6901b" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> OFO North Yuba Stand 1 </a> by <a href="https://sketchfab.com/djnyoung" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> djnyoung </a> on <a href="https://sketchfab.com" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p></div>


## Variable-radius local maximum filter { #lmf }

An algorithm that searches each pixel in a canopy height model to determine whether it is a local maximum (i.e., a predicted treetop) by comparing its height to neighboring pixels. The neighboring pixels that are checked are those within a radius that varies based on the height of the pixel being evaluated. The relationship between the pixel's height and the radius of the search area is defined by a user-specified function.

![Local maximum filter](/assets/images/tutorials/lmf.png)