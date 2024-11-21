#!/usr/bin/env python3
"""
konsole-distrobox-integration

targets.py: classes and interfaces for profile creation from specs.

Author: jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__package__ = "konsoledistroboxintegration"

from abc import ABC, abstractmethod
from typing import List, Dict
from pathlib import Path

from konsoledistroboxintegration.profiles import Profile
from konsoledistroboxintegration.files import (
    directory_exists,
    merge_file_tree,
    FileSpec,
)
from konsoledistroboxintegration.commands import command_exists
from konsoledistroboxintegration.manifests import make_manifest


class ProfileTarget(ABC):
    @abstractmethod
    def __init__(self, current_user: str) -> None:
        """
        Generic constructor.

        Args:
            current_user (str): username of the current user.
        """
        pass

    @abstractmethod
    def get_target_name(self) -> str:
        """
        Get an identifying string name for the target.

        Returns:
            str: the name.
        """
        pass

    @abstractmethod
    def make_targets(self, profiles: List[Profile]) -> None:
        """
        Process a list of profiles into files or entries.

        Returns:
            List[Profile]: the list of Profiles.
        """
        pass

    @abstractmethod
    def check_dependencies(self) -> bool:
        """
        Checks if external dependencies for the target
        are satisfied, and returns a boolean result.

        Returns:
            bool: True is all dependencies are satisfied.
        """
        pass


class KonsoleTarget(ProfileTarget):
    def __init__(self, current_user: str) -> None:
        self.current_user = current_user
        self.profiles_dir = Path.home() / ".local/share/konsole"
        self.rc_file = Path.home() / ".config/konsolerc"

    def get_target_name(self) -> str:
        return "konsole"

    def get_parent_profile(self) -> str:
        """
        Get the parent profile for a Konsole profile, either
        the main Konsole profile, or "FALLBACK/" if it cannot
        be determined.

        Returns:
            str: the parent Konsole profile.
        """
        if not self.rc_file.is_file():
            return "FALLBACK/"
        with open(self.rc_file, "r") as f:
            lines = [
                line.split("=")[1]
                for line in f.readlines()
                if line.startswith("DefaultProfile=")
            ]
            if len(lines) < 1:
                return "FALLBACK/"
            return Path.home() / f".local/share/konsole/{lines[0]}"

    #     def make_profile(self, profile: Profile) -> FileSpec:
    #         return f"""
    # [General]
    # Command={profile.exec_command}{f"\nIcon={profile.icon}" if profile.icon is not None else ""}
    # Name={profile.get_friendly_name()}
    # Parent={self.get_parent_profile()}
    #         """.strip()

    def make_config_file(self, profile: Profile) -> str:
        """
        Create and return the contents of a Konsole profile from
        a profile spec.

        Args:
            profile (Profile): the Profile spec object.

        Returns:
            str: the .profile file contents.
        """
        return f"""
[General]
Command={profile.exec_command}{f"\nIcon={profile.icon}" if profile.icon is not None else ""}
Name={profile.get_friendly_name()}
Parent={self.get_parent_profile()}
        """.strip()

    def make_targets(self, profiles: List[Profile]) -> None:
        make_manifest(self.profiles_dir, profiles)
        merge_file_tree(
            root=self.profiles_dir,
            glob=Profile.get_file_glob("profile"),
            specs=[
                FileSpec(
                    self.make_config_file(p),
                    p.get_file_path(self.profiles_dir, "profile"),
                )
                for p in profiles
            ],
        )

    def check_dependencies(self) -> bool:
        return all([command_exists("konsole"), directory_exists(self.profiles_dir)])


def get_targets(query: List[str], current_user: str) -> Dict[str, ProfileTarget]:
    """
    VESTIGIAL; Returns target objects that match a query.
    """
    all_sources = [KonsoleTarget(current_user)]
    if "all" in query:
        return all_sources
    return [s for s in all_sources if s.get_target_name() in query]
