#!/usr/bin/env python3
"""
konsole-distrobox-integration

core.py: contains core appliction functions for profile generation
         and log watching.

Author: jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__package__ = "konsoledistroboxintegration"

import logging
from typing import Callable, List
from shutil import which
from subprocess import Popen, PIPE, STDOUT

from konsoledistroboxintegration.commands import command_exists
from konsoledistroboxintegration.sources import DistroboxProfileGenerator
from konsoledistroboxintegration.targets import get_targets


def generate_profiles(current_user: str, target_query: List[str]) -> None:
    """
    Generates Konsole profiles from Distrobox containers.

    Args:
        current_user (str): the currently logged-in user, required for
                            reading/writing profile files.
        target_query (List[str]): the target query -- insignificant for
                                  now, should always be ["all"] or
                                  ["konsole"]
    """
    source = DistroboxProfileGenerator(current_user)
    if not source.check_dependencies():
        logging.error("distrobox: Missing dependencies.")
        exit(1)
    profiles = source.get_profiles()
    targets = get_targets(target_query, current_user)
    for t in targets:
        if not t.check_dependencies():
            logging.warn(
                f"{t.get_target_name()} cannot be run due to missing dependencies."
            )
            continue
        t.make_targets(profiles)


def watch_journal(callback: Callable) -> None:
    """
    Read systemd journal for podman events, and run the callback when
    a new event occurs.

    Args:
        callback (Callable): The callback, usually a wrapping of
                             `generate_profiles`
    """
    if not command_exists("journalctl"):
        logging.fatal("Cannot run watcher: journalctl missing.")
        exit(1)
    if not command_exists("podman"):
        logging.fatal("Cannot run watcher: podman missing.")
        exit(1)
    logging.info("Following journal for podman events.")
    command = [which("journalctl"), "--follow", "--lines", "0", which("podman")]
    process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=False)
    try:
        for line in process.stdout:
            line_text = line.decode("utf-8")
            if "container" not in line_text:
                continue
            if "create" in line_text:
                logging.info("Podman event: distrobox-create likely ran.")
            if "remove" in line_text:
                logging.info("Podman event: distrobox-create likely ran.")
            callback()
        process.wait()
    except KeyboardInterrupt:
        print()
        logging.info("Watcher interrupted by SIGINT, now exiting.")
        exit(0)
