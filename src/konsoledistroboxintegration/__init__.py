#!/usr/bin/env python3
"""
konsole-distrobox-integration

__init__.py: main CLI entry point.

Author: jahinzee <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

__package__ = "konsoledistroboxintegration"

import logging
from sys import stderr
from argparse import ArgumentParser, Namespace
from os import geteuid
from getpass import getuser

from konsoledistroboxintegration.core import generate_profiles, watch_journal


def configure_logs(show_all: bool) -> None:
    """
    Configure logging information, including target level and format.

    Args:
        show_all (bool): set output to show all levels, else only
                         warnings
    """
    level = logging.INFO if show_all else logging.WARNING
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s] %(message)s", stream=stderr, level=level
    )


def get_user() -> str | None:
    """
    Returns the current user's username. Fatally exits if user is root.

    Returns:
        str | None: the username.
    """
    ROOT_UID = 0
    if geteuid() == ROOT_UID:
        logging.fatal("konsole-distrobox-integration cannot run as root.")
        exit(0)
    return getuser()


def get_args() -> Namespace:
    """
    Parses and returns program arguments. See function body (or help
    output) for more information.

    Returns:
        Namespace: the argparse Namespace containing argument data.
    """
    parser = ArgumentParser(
        prog="konsole-distrobox-integration",
        description="Generate Konsole profiles from Distrobox containers.",
    )
    parser.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="watch journal for Podman updates and regenerate accordingly",
    )
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="output all non-error log information to console",
    )
    return parser.parse_args()


def main() -> None:
    """
    The main script routine.
    """
    current_user = get_user()
    args = get_args()
    configure_logs(args.log)
    callback = lambda: generate_profiles(current_user, ["konsole"])  # noqa: E731
    if args.watch:
        watch_journal(callback)
        return
    callback()


if __name__ == "__main__":
    main()
