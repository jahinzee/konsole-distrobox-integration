#!/usr/bin/env python3
"""
konsole-distrobox-integration

profiles.py: dataclass for representing profile specs.

Author: jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__package__ = "konsoledistroboxintegration"

from typing import Optional, Self
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Profile:
    name: str
    source: str
    icon: Optional[Path]
    exec_command: str

    def to_dict(self) -> dict[str, str]:
        """
        Creates a dictionary representation for manifest files.

        Returns:
            dict[str, str]: the dict representation.
        """
        if self.icon is None:
            return {
                "name": self.name,
                "source": self.source,
                "exec": self.exec_command,
            }
        return {
            "name": self.name,
            "source": self.source,
            "icon": str(self.icon),
            "exec": self.exec_command,
        }

    def get_root_name(self) -> str:
        """
        Gets the profile root name, for filename and internal identification.

        Returns:
            str: the root name
        """
        return f"{self.source}-{self.name}"

    def get_file_path(self, directory: Path, suffix: str) -> Path:
        """
        Get a filename from the root name, attaching the directory
        and suffix.

        Args:
            directory (Path): the directory to place the file in.
            suffix (str): the suffix (e.g. ".profile")

        Returns:
            Path: the target path.
        """
        return Path(
            directory / f"konsole-distrobox-integration-{self.get_root_name()}.{suffix}"
        )

    def get_friendly_name(self) -> str:
        """
        Get a friendly name for the profile, for naming at the UI level.

        Returns:
            str: _description_
        """
        return f"{self.source} – {self.name}"

    @staticmethod
    def get_file_glob(suffix: str) -> str:
        """
        Returns a file glob that matches for `get_root_name` with a suffix.

        Args:
            suffix (str): the suffix (e.g. ".profile")

        Returns:
            str: a glob string that matches the root name.
        """
        return f"konsole-distrobox-integration-*-*.{suffix}"

    @staticmethod
    def from_dict(source: dict[str, str]) -> Self:
        """
        Reconstructs a Profile object from a dictionary
        generated from `to_dict`.

        Args:
            source (dict[str, str]): the source dictionary.

        Returns:
            Self: the reconstructed Profile object.
        """
        return Profile(
            name=source["name"],
            source=source["source"],
            icon=source["icon"] if "icon" in source else None,
            exec_command=source["exec"],
        )
