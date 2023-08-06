# Rammon (RAM Monitor)

Rammon is a tool to alert you when your machine is running low on memory with a desktop notification.

![Rammon Screenshot](https://raw.githubusercontent.com/jackadamson/rammon/master/screenshots/screenshot1.png)

Notifications are sent using dbus meaning it's supported by a wide range of Linux window managers
such as Gnome, KDE and many more.

## Requirements

- Linux
- Python3.6
- systemd (required for auto-start)
- PyGI (not packaged on pypi, python3-gi for Ubuntu, python-gobject for ArchLinux)
- GLib 2.46+ and girepository 1.46+

## Usage

```
rammon [-h | --help] [-d | --no-daemon] [--set OPTION=value] [command]

    Commands are:
       start      Start the memory monitor
       stop       Stop the memory monitor
       status     Check the status of the memory monitor
       enable     Set rammon to run on login as a systemd user service
       disable    Disable rammon's auto-start
       config     Get and set configuration options

    Check command options with:
       rammon <command> -h

```
