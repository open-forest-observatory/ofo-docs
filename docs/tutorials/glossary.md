---
weight: 100
# To make a term linkable from any page by writing it in square brackets, add
# it (and any variants, e.g. plurals) to includes/glossary-links.md, pointing
# to its heading anchor.
---

# Glossary

This page defines common technical terms used in the OFO tutorials. TODO: Expand on these definitions.

## Canopy height model (CHM) { #chm }

A raster data product that represents the height of vegetation above the ground surface.

## Orthomosaic { #orthomosaic }

A georeferenced image created by stitching together multiple overlapping aerial photographs. It is a geospatial data product, allowing for precise measurements and analysis using GIS tools.

## Variable-radius local maximum filter { #lmf }

An algorithm that searches each pixel in a canopy height model to determine whether it is a local maximum (i.e., a treetop) by comparing its height to neighboring pixels. The neighboring pixels that are checked are those within a radius that varies based on the height of the pixel being evaluated. The relationship between the pixel's height and the radius of the search area is defined by a user-specified function.
