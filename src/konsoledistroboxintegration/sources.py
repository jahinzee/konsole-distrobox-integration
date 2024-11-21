#!/usr/bin/env python3
"""
konsole-distrobox-integration

sources.py: classes and interfaces for profile spec generators.

Author: jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__package__ = "konsoledistroboxintegration"

from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path
import logging

from konsoledistroboxintegration.profiles import Profile
from konsoledistroboxintegration.commands import run_command, command_exists


class ProfileSource(ABC):
    @abstractmethod
    def __init__(self, current_user: str) -> None:
        """
        Generic constructor.

        Args:
            current_user (str): username of the current user.
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get an identifying string name for the source.

        Returns:
            str: the name.
        """
        pass

    @abstractmethod
    def get_profiles(self) -> List[Profile]:
        """
        Get a list of profiles to generate.

        Returns:
            List[Profile]: the list of Profiles.
        """
        pass

    @abstractmethod
    def check_dependencies(self) -> bool:
        """
        Checks if external dependencies for the source
        are satisfied, and returns a boolean result.

        Returns:
            bool: True is all dependencies are satisfied.
        """
        pass


class DistroboxProfileGenerator(ProfileSource):
    """
    Profile generator for Distrobox containers.
    See docstrings for `ProfileSource` for more information.
    """

    def __init__(self, current_user: str) -> None:
        self.current_user = current_user

    def get_source_name(self) -> str:
        return "distrobox"

    def get_icon(self, image_path: str) -> Optional[Path]:
        """
        Return an icon path (if available) for the Distrobox
        container image, from the same source as used in
        `distrobox-generate-entry`.

        Args:
            image_path (str): The full image name

        Returns:
            Optional[Path]: a valid icon path, or None if it
                            doesn't exist.
        """
        image_path_base = image_path.split("/")[-1].split(":")[0]

        icons_folder = Path.home() / ".local/share/icons/distrobox"
        if not icons_folder.is_dir():
            return None

        for path in icons_folder.iterdir():
            if path.stem == image_path_base:
                return path
        return None

    def get_profiles(self) -> List[Profile]:
        NAME, IMAGE = 1, 3
        output = run_command(["distrobox", "list"]).splitlines()[1:]
        boxes = [[w.strip() for w in o.split("|")] for o in output]
        logging.info("distrobox: Generated profiles:")
        for b in boxes:
            logging.info(f"  - {b[NAME]}")
        return [
            Profile(
                name=b[NAME],
                source=self.get_source_name(),
                icon=self.get_icon(b[IMAGE]),
                exec_command=f"distrobox enter {b[NAME]}",
            )
            for b in boxes
        ]

    def check_dependencies(self) -> bool:
        return all([command_exists("distrobox")])


# class SSHProfileGenerator(ProfileSource):
#     def __init__(self, current_user: str) -> None:
#         self.current_user = current_user
#         self.ssh_config_filepath = Path(f"/home/{current_user}/.ssh/config")

#     def get_source_name(self) -> str:
#         return "ssh"

#     def get_profiles(self) -> List[Profile]:
#         with open(self.ssh_config_filepath, "r") as ssh_config_file:
#             hosts = [
#                 line.strip().split(" ")[1]
#                 for line in ssh_config_file.readlines()
#                 if line.startswith("Host")
#             ]
#             return [
#                 Profile(name=h, source="ssh", icon=None, exec_command=f"ssh {h}")
#                 for h in hosts
#             ]

#     def check_dependencies(self) -> bool:
#         return all([command_exists("ssh"), file_exists(self.ssh_config_filepath)])
