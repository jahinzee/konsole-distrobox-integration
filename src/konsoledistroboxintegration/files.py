#!/usr/bin/env python3
"""
konsole-distrobox-integration

files.py: functions for managing profile spec files and folders.

Author: jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__package__ = "konsoledistroboxintegration"

import logging
from typing import Optional, NamedTuple, List
from pathlib import Path


def write_file_sparingly(
    content: str,
    filepath: Path,
    ignore_lines: Optional[int],
    no_compare: Optional[bool],
) -> None:
    """
    Write contents to a file, unless the contents already match.

    Args:
        content (str): the file contents.
        filepath (Path): the target file path.
        ignore_lines (Optional[int]): lines to ignore (from the start)
                                      when comparing contents -- useful
                                      for skipping comments
        no_compare (Optional[bool]): do not compare files, always write
    """
    if ignore_lines is None:
        ignore_lines = 0
    if filepath.is_file():
        if no_compare:
            logging.info(f"File {str(filepath)} exists - skipping writing...")
            return
        with open(filepath, "r") as f:
            # Adapted from: https://stackoverflow.com/a/17060409
            saved_content = f.read()
            saved_content_trimmed = "\n".join(saved_content.split("\n")[ignore_lines:])
            content_trimmed = "\n".join(content.split("\n")[ignore_lines:])
            if saved_content_trimmed == content_trimmed:
                logging.info(f"File {str(filepath)} unchanged - skipping writing...")
                return
    with open(filepath, "w") as fw:
        fw.write(content)


def directory_exists(path: Path) -> bool:
    """
    Check if directory at path exists.

    Args:
        path (Path): the path to check.

    Returns:
        bool: True if directory exists.
    """
    return path.is_dir()


class FileSpec(NamedTuple):
    content: str
    path: Path


def merge_file_tree(root: Path, glob: str, specs: List[FileSpec]) -> None:
    """
    Write a tree of files (defined in Filespec) to the root directory,
    and deletes stray files (as defined in `glob`).

    Args:
        root (Path): the root directory.
        glob (str): the glob of existing files to match. If a file
                    in `root` matches but isn't accounted for in
                    `specs`, it is deleted.
        specs (List[FileSpec]): The filepath and contents to write.
    """
    current_filetree = [fn for fn in root.glob(glob) if fn.is_file()]

    new_filetree = [s.path for s in specs]
    logging.info("Files to create/update:")
    if len(new_filetree) < 1:
        logging.info("  (none)")
    for f in new_filetree:
        logging.info(f"  - {str(f)}")

    files_to_delete = [fn for fn in current_filetree if fn not in new_filetree]
    logging.info("Files to delete:")
    if len(files_to_delete) < 1:
        logging.info("  (none)")
    for f in files_to_delete:
        logging.info(f"  - {str(f)}")

    for content, path in specs:
        write_file_sparingly(content, path, ignore_lines=0, no_compare=True)

    for fn in files_to_delete:
        logging.info(f"Deleting file: {str(fn)}")
        fn.unlink(missing_ok=True)
