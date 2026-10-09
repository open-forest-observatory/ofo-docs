#!/usr/bin/env python3
"""
Download the zipped raw drone imagery for a mission from the OFO object store, extract it
in place, and delete the zip.

The zip is downloaded with rclone, using its on-the-fly backend syntax (:s3:) so no
pre-configured remote is needed. S3 credentials are read from environment variables
(S3_ENDPOINT, RCLONE_S3_ACCESS_KEY_ID, RCLONE_S3_SECRET_ACCESS_KEY, and optionally
S3_PROVIDER) so that they are not exposed in the process list.

Usage:
    python 1_download-raw-images.py
"""

import os
import shutil
import subprocess
import sys

# S3 paths (format: 'bucket/path/to/file.zip') of the imagery zips to download. Each zip is
# extracted into a folder under DOWNLOAD_ROOT named after the zip, minus the
# '_images.zip' suffix (e.g. '000448_images.zip' -> '000448').
S3_PATHS = [
    "ofo-public/drone/missions_03/000448/images/000448_images.zip",
    "ofo-public/drone/missions_03/000452/images/000452_images.zip",
]
DOWNLOAD_ROOT = "/ofo-share/project-data/tutorial-data/pre-tutorial-data/raw-drone-photos"

REQUIRED_S3_ENV_VARS = [
    "S3_ENDPOINT",
    "RCLONE_S3_ACCESS_KEY_ID",
    "RCLONE_S3_SECRET_ACCESS_KEY",
]


def validate_environment():
    """Check that the S3 credential environment variables and rclone are available."""
    missing_vars = [var for var in REQUIRED_S3_ENV_VARS if not os.environ.get(var)]
    if missing_vars:
        print(
            f"Error: Missing required environment variables: {' '.join(missing_vars)}"
        )
        sys.exit(1)

    if shutil.which("rclone") is None:
        print("Error: rclone not found")
        sys.exit(1)


def get_s3_flags():
    """Build common S3 flags for rclone commands.

    Credentials are not passed as flags: rclone reads RCLONE_S3_ACCESS_KEY_ID and
    RCLONE_S3_SECRET_ACCESS_KEY from the environment directly.
    """
    return [
        "--s3-provider",
        os.environ.get("S3_PROVIDER", "Other"),
        "--s3-endpoint",
        os.environ.get("S3_ENDPOINT"),
    ]


def download_s3(s3_path, download_dir):
    """Download a file from S3 (format: 'bucket/path/to/file') into download_dir."""
    filename = s3_path.rstrip("/").split("/")[-1]
    local_path = os.path.join(download_dir, filename)

    print(f"Downloading: {s3_path}")
    print(f"  -> {local_path}")

    cmd = [
        "rclone",
        "copyto",
        f":s3:{s3_path}",
        local_path,
        "--progress",
        "--retries",
        "5",
        "--retries-sleep",
        "15s",
    ] + get_s3_flags()

    subprocess.run(cmd, check=True)

    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Download completed but file not found: {local_path}")

    file_size = os.path.getsize(local_path)
    print(f"  Downloaded: {file_size / (1024*1024):.1f} MB")

    return local_path


def extract_zip(zip_path, extract_dir):
    """Extract a zip file into extract_dir."""
    print(f"Extracting: {zip_path}")
    print(f"  -> {extract_dir}")

    # -o: overwrite without prompting
    # -q: quiet mode (less verbose, but errors still shown)
    cmd = ["unzip", "-o", "-q", zip_path, "-d", extract_dir]

    subprocess.run(cmd, check=True)

    print("  Extraction complete")


def delete_zip(zip_path):
    """Delete a zip file to save space."""
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"  Deleted zip: {zip_path}")


def main():
    validate_environment()

    for i, s3_path in enumerate(S3_PATHS, 1):
        print(f"\n[{i}/{len(S3_PATHS)}] Processing: {s3_path}")

        filename = s3_path.rstrip("/").split("/")[-1]
        folder_name = filename.removesuffix(".zip").removesuffix("_images")
        download_dir = os.path.join(DOWNLOAD_ROOT, folder_name)

        os.makedirs(download_dir, exist_ok=True)
        zip_path = download_s3(s3_path, download_dir)
        extract_zip(zip_path, download_dir)
        delete_zip(zip_path)


if __name__ == "__main__":
    main()
