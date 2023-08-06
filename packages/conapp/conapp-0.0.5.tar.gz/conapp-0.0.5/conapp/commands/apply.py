import os
import argparse
import sys

from conapp.url_generators import RESOLVERS
from conapp.file_paths import get_repo_dir
from conapp.definitions import Hosts
from conapp.file_paths import check_dirs, create_dirs
from conapp.file_ops import apply_snapshot, create_snapshot, download_file

COMMAND = 'apply'


def setup_arguments(sub_parser) -> argparse.ArgumentParser:
    """
    Setup the arguments for the apply command
    """
    parser = sub_parser.add_parser(COMMAND, help="apply a config")

    parser.set_defaults(command=main)
    parser.add_argument(
        '-u',
        '--user',
        required=True,
        help='username to pull from'
    )
    parser.add_argument(
        '-r',
        '--repo',
        default='config',
        help='repo name to pull, defaults to config'
    )
    parser.add_argument(
        '--no-download',
        action='store_true',
        help='Use already downloaded copy'
    )
    parser.add_argument(
        '-b',
        '--bitbucket',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.BITBUCKET,
        help='pull from bitbucket'
    )
    parser.add_argument(
        '-g',
        '--github',
        action='store_const',
        dest='host',
        default=Hosts.GITHUB,
        const=Hosts.GITHUB,
        help='pull from bitbucket'
    )
    parser.add_argument(
        '--dry-run',
        action="store_true",
        dest="dry_run",
        help="Don't actually run"
    )

    #TODO: Add in a --no-apply flag to have it just download

    return parser


def main(args: argparse.Namespace) -> None:
    """Download and Apply a snapshot"""
    repo_dir = get_repo_dir(args.user, args.repo)

    if not check_dirs([repo_dir]):
        create_dirs([repo_dir])

    file_name = repo_dir + "/" + f"{args.user}.{args.repo}.tar.gz"

    if args.no_download and os.path.isfile(file_name):
        print(f"no-download passed, applying local file {file_name}")
    else:
        if args.no_download:
            print("Error: no-download passed but no local copy to apply!")
            sys.exit(2)
        else:
            download_file(
                file_name,
                RESOLVERS.get(args.host)(args.user, args.repo)
            )

    if args.dry_run:
        print(f"dry run, applying {file_name}")
    else:
        create_snapshot(file_name)
        apply_snapshot(file_name)

