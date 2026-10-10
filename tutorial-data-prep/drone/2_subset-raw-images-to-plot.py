#!/usr/bin/env python3
"""
Subset the raw drone photos downloaded by 1_download-raw-images.py to only those taken
within a buffered ground-reference plot boundary, and copy them into a separate folder per
mission.

Photo locations are read from the GPS tags in each photo's EXIF metadata. The plot
boundary and photo locations are projected to a local UTM CRS so the buffer can be applied
in meters. The folder structure within each mission folder (sub-mission and camera
subfolders) is preserved in the output. The buffered plot boundary is also saved, for use as
the mission boundary when postprocessing the photogrammetry products.

Requires: geopandas, Pillow

Usage:
    python 2_subset-raw-images-to-plot.py
"""

import os
import shutil

import geopandas as gpd
from PIL import Image

# Mission folders created by 1_download-raw-images.py. Each is subset into a folder under
# OUTPUT_ROOT named after the mission folder plus 'clip' (e.g. '000448' -> '000448clip').
MISSION_DIRS = [
    "/ofo-share/project-data/tutorial-data/pre-tutorial-data/raw-drone-photos/000448",
    "/ofo-share/project-data/tutorial-data/pre-tutorial-data/raw-drone-photos/000452",
]
PLOT_BOUNDARY_PATH = "/ofo-share/project-data/tutorial-data/tutorial-data/inputs/ground-reference/ofo-ground-reference-plot_0030.gpkg"
# Distance (meters) beyond the plot boundary within which photos are kept
BUFFER_M = 60
OUTPUT_ROOT = "/ofo-share/project-data/tutorial-data/tutorial-data/inputs/drone/raw-drone-photos"
BOUNDARY_OUTPUT_PATH = "/ofo-share/project-data/tutorial-data/tutorial-data/inputs/drone/boundaries/composite1_boundary.gpkg"

PHOTO_EXTENSIONS = (".jpg", ".jpeg", ".tif", ".tiff")

# EXIF tag IDs
GPS_IFD_TAG = 0x8825
GPS_LATITUDE_REF = 1
GPS_LATITUDE = 2
GPS_LONGITUDE_REF = 3
GPS_LONGITUDE = 4


def find_photos(mission_dir):
    """Recursively list all photo files in mission_dir, sorted by path."""
    photo_paths = []
    for dirpath, _, filenames in os.walk(mission_dir):
        for filename in filenames:
            if filename.lower().endswith(PHOTO_EXTENSIONS):
                photo_paths.append(os.path.join(dirpath, filename))
    return sorted(photo_paths)


def dms_to_decimal(dms, ref):
    """Convert an EXIF (degrees, minutes, seconds) tuple and hemisphere ref to decimal degrees."""
    degrees, minutes, seconds = (float(x) for x in dms)
    decimal = degrees + minutes / 60 + seconds / 3600
    return -decimal if ref in ("S", "W") else decimal


def get_photo_coords(photo_path):
    """Return (lon, lat) in decimal degrees from a photo's EXIF GPS tags, or None if absent."""
    with Image.open(photo_path) as img:
        gps = img.getexif().get_ifd(GPS_IFD_TAG)

    if not all(tag in gps for tag in (GPS_LATITUDE, GPS_LONGITUDE)):
        return None

    lat = dms_to_decimal(gps[GPS_LATITUDE], gps.get(GPS_LATITUDE_REF, "N"))
    lon = dms_to_decimal(gps[GPS_LONGITUDE], gps.get(GPS_LONGITUDE_REF, "E"))
    return lon, lat


def load_buffered_boundary():
    """Load the plot boundary, project it to a local UTM CRS, and buffer it by BUFFER_M."""
    plot = gpd.read_file(PLOT_BOUNDARY_PATH)
    plot = plot.to_crs(plot.estimate_utm_crs())
    buffered = plot.geometry.union_all().buffer(BUFFER_M)
    return buffered, plot.crs


def subset_mission(mission_dir, boundary, boundary_crs):
    """Copy the photos in mission_dir that fall within boundary into the mission's subset folder."""
    photo_paths = find_photos(mission_dir)
    print(f"  Found {len(photo_paths)} photos")

    lons, lats, located_paths = [], [], []
    for photo_path in photo_paths:
        coords = get_photo_coords(photo_path)
        if coords is None:
            print(f"  Warning: no GPS tags, skipping: {photo_path}")
            continue
        lons.append(coords[0])
        lats.append(coords[1])
        located_paths.append(photo_path)

    photos = gpd.GeoDataFrame(
        {"path": located_paths},
        geometry=gpd.points_from_xy(lons, lats),
        crs="EPSG:4326",
    ).to_crs(boundary_crs)
    photos_in_plot = photos[photos.within(boundary)]
    print(f"  {len(photos_in_plot)} photos within {BUFFER_M} m of the plot boundary")

    mission_id = os.path.basename(os.path.normpath(mission_dir))
    output_dir = os.path.join(OUTPUT_ROOT, f"{mission_id}clip")
    print(f"  Copying to: {output_dir}")

    for photo_path in photos_in_plot["path"]:
        dest_path = os.path.join(output_dir, os.path.relpath(photo_path, mission_dir))
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(photo_path, dest_path)

    print("  Copy complete")


def save_boundary(boundary, boundary_crs):
    """Save the buffered plot boundary to BOUNDARY_OUTPUT_PATH."""
    os.makedirs(os.path.dirname(BOUNDARY_OUTPUT_PATH), exist_ok=True)
    gpd.GeoDataFrame(geometry=[boundary], crs=boundary_crs).to_file(BOUNDARY_OUTPUT_PATH)
    print(f"Saved buffered plot boundary to: {BOUNDARY_OUTPUT_PATH}")


def main():
    boundary, boundary_crs = load_buffered_boundary()
    save_boundary(boundary, boundary_crs)

    for i, mission_dir in enumerate(MISSION_DIRS, 1):
        print(f"\n[{i}/{len(MISSION_DIRS)}] Processing: {mission_dir}")
        subset_mission(mission_dir, boundary, boundary_crs)


if __name__ == "__main__":
    main()
