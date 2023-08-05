import argparse
import os
import sys
from typing import List

from litefeel.pycommon.io import read_file

from .config import Config
from .subcommands import adbdevice, adbpush, apkinfo, apkinstall

_VERSION_FILE_NAME = "version.txt"


def get_version():
    dir_of_this_script = os.path.split(__file__)[0]
    version_file_path = os.path.join(dir_of_this_script, _VERSION_FILE_NAME)
    return read_file(version_file_path).strip()


class Command:
    def __init__(self, name: str, command, help):
        self.name = name
        self.command = command
        self.help = help


def addsubcommands(subparser: argparse._SubParsersAction, commands: List[Command]):
    for cmd in commands:
        parser = subparser.add_parser(cmd.name, help=cmd.help)
        parser.set_defaults(docommand=cmd.command.docommand)
        cmd.command.addcommand(parser)


def add_global_params(parser: argparse.ArgumentParser):
    parser.add_argument("-c", "--config", dest="config", help="global config")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {get_version()}"
    )


def main(args=None):
    parser = argparse.ArgumentParser(
        usage="%(prog)s [options]", description="show android device list"
    )

    add_global_params(parser)

    commands = [
        Command("devices", adbdevice, "show android device list"),
        Command("push", adbpush, "push files to android device"),
        Command("install", apkinstall, "install apk file"),
        Command("apk", apkinfo, "show apk packageName/activityName"),
    ]

    subparser = parser.add_subparsers(title="sub commands", dest="subcommand")
    addsubcommands(subparser, commands)

    args = parser.parse_args(args)
    if args.subcommand is None:
        parser.print_help()
        exit(0)

    cfg = Config()
    if args.config is not None:
        cfg.load_config(args.config)
    args.docommand(args, cfg)


# -------------- main ----------------
if __name__ == "__main__":
    main()
