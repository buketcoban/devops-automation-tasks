#!/usr/bin/env python3

import argparse
import logging
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Clean a ZIP archive by removing folders without __init__.py'
    )
    parser.add_argument(
        'zip_file',
        help='Path to the ZIP archive to clean'
    )
    return parser.parse_args()


def validate_zip_file(zip_path):
    if not os.path.exists(zip_path):
        logging.error(f"ZIP file does not exist: {zip_path}")
        sys.exit(1)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.testzip()
    except zipfile.BadZipFile:
        logging.error(f"Invalid ZIP file: {zip_path}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error validating ZIP file: {e}")
        sys.exit(1)


def extract_zip(zip_path, extract_dir):
    logging.info(f"Extracting ZIP archive: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(extract_dir)
    logging.info(f"Extracted to temporary directory: {extract_dir}")


def clean_folders(root_dir):
    root_path = Path(root_dir)
    removed_folders = []

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        dir_path = Path(dirpath)

        if dir_path == root_path:
            continue

        if '__init__.py' not in filenames:
            rel_path = dir_path.relative_to(root_path)
            rel_path_str = str(rel_path).replace(os.sep, '/')

            logging.info(f"Removing folder (no __init__.py): {rel_path_str}")
            shutil.rmtree(dir_path)
            removed_folders.append(rel_path_str)

    removed_folders.sort()
    return removed_folders


def create_cleaned_txt(root_dir, removed_folders):
    cleaned_file = Path(root_dir) / 'cleaned.txt'

    with open(cleaned_file, 'w') as f:
        for folder in removed_folders:
            f.write(f"{folder}\n")

    logging.info(f"Created cleaned.txt at: {cleaned_file}")


def create_new_zip(root_dir, original_zip_path):
    original_path = Path(original_zip_path)
    new_zip_name = original_path.stem + '_new' + original_path.suffix
    new_zip_path = original_path.parent / new_zip_name

    logging.info(f"Creating new archive: {new_zip_path}")

    with zipfile.ZipFile(new_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        root_path = Path(root_dir)

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dir_path = Path(dirpath)

            for filename in filenames:
                file_path = dir_path / filename
                arcname = file_path.relative_to(root_path)
                arcname_str = str(arcname).replace(os.sep, '/')
                zf.write(file_path, arcname_str)

    logging.info(f"New archive created: {new_zip_path}")
    return new_zip_path


def main():
    setup_logging()

    logging.info("Starting clean_app.py")

    args = parse_arguments()
    zip_file = args.zip_file

    logging.info(f"Input archive: {zip_file}")

    validate_zip_file(zip_file)

    with tempfile.TemporaryDirectory() as temp_dir:
        logging.info(f"Using temporary directory: {temp_dir}")

        extract_zip(zip_file, temp_dir)

        items = list(Path(temp_dir).iterdir())
        if len(items) == 1 and items[0].is_dir():
            root_dir = items[0]
        else:
            root_dir = Path(temp_dir)

        logging.info(f"Root directory for cleaning: {root_dir}")

        removed_folders = clean_folders(str(root_dir))

        create_cleaned_txt(str(root_dir), removed_folders)

        create_new_zip(str(root_dir), zip_file)

    logging.info("Cleaning process completed successfully")


if __name__ == '__main__':
    main()
