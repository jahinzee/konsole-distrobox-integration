# `konsole-distrobox-integration`

A utility and service for automatic integration of Distrobox containers
into Konsole profiles (and by extension: Dolphin, Kate, Yakuake, etc.).

This project is not affiliated with KDE e.V. or Distrobox.

> [!IMPORTANT]
> The application is intended for use with a Podman backend.
> Docker and Lilipod backends are currently not supported.

## Installation

Use either `pipx` (recommended) or `pip`.

```sh
$ pipx install git+https://github.com/jahinzee/konsole-distrobox-integration.git
```

## Usage

### Standalone

Running the script standalone will perform a profile update; getting the
output of `distrobox list`, generating Konsole profiles, and deleting any stray
profile listings.

```sh
$ konsole-distrobox-integration
```

Note that Konsole may not update its own profile list until next launch.
You may need to restart Konsole for the profile updates to take effect.

### As a Service

> [!IMPORTANT]
> The watch mode requires `journalctl`, and therefore will not
> work on systems without systemd.

The script can also run in watch mode, listening for Podman events
through the journal, and recreating profiles when a Podman container
is created or deleted.

Use the `-w`/`--watch` flag to run in watch mode. You can also
combine it with `-l`/`--log` for more vebose logging.

```sh
$ konsole-distrobox-integration -wl
```

#### Autostart

For better integration, you can configure your system to run this script
on login in watch mode. This can be done by either:

- create an entry in [KDE Plasma's Autostart settings](https://userbase.kde.org/index.php?title=System_Settings/Autostart), or
- create and activate a [systemd user service](https://linuxhandbook.com/create-systemd-services/).
