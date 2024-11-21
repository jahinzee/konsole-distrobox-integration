#!/usr/bin/env python3
"""
konsole-distrobox-integration

commands.py: functions for wrapping shutil and subprocess.

Author: jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__package__ = "konsoledistroboxintegration"

from typing import List
from subprocess import run, PIPE
from shutil import which


def run_command(command: List[str]) -> str:
    """
    Runs a command with subprocess, and return stdout as UTF-8.

    Args:
        command (List[str]): the command to run, as list with arguments.

    Returns:
        str: UTF-8 output of command.
    """
    return run(command, stdout=PIPE).stdout.decode("utf-8")


def command_exists(command: str) -> bool:
    """
    Checks if command/application is available in PATH.

    Args:
        command (str): the application binary name

    Returns:
        bool: True if application exists in PATH, else false.
    """
    return which(command) is not None
