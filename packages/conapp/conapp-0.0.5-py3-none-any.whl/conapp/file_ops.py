import subprocess
import os
import urllib.request
import sys

from conapp.file_paths import get_snapshot_filename
from conapp.validate import validate_subprocess
from conapp.definitions import USER_HOME_DIR, DEFAULT_STRIP_COMPONENTS


def apply_snapshot(file_name: str) -> None:
    """Given file_name use tar to apply it to the users home directory"""
    if not os.path.isfile(file_name):
        print(f"Error! attempted to apply nonexistent snapshot {file_name}")

    print(f"Applying snapshot {file_name}")

    validate_subprocess(
        subprocess.run([
            'tar',
            '-C',
            USER_HOME_DIR,
            DEFAULT_STRIP_COMPONENTS,
            '--show-transformed-names',
            '-zvxf',
            file_name,
        ])
    )


def create_snapshot(file_name):
    get_file_names_command = [
        "tar",
        DEFAULT_STRIP_COMPONENTS,
        '--show-transformed-names',
        '-tf',
        file_name
    ]
    get_file_names_command_result = subprocess.run(
        get_file_names_command,
        text=True,
        capture_output=True
    )

    validate_subprocess(get_file_names_command_result)

    files = list(
        filter(
            lambda file_path: os.path.isfile(
                os.path.expanduser(f"~/{file_path}")),
            get_file_names_command_result.stdout.split()
        )
    )

    if len(files) > 0:
        snapshot_name = get_snapshot_filename()
        backup_command = [
                             'tar',
                             '-C',
                             USER_HOME_DIR,
                             '-czvf',
                             snapshot_name,
                         ] + files

        print(f"Local files would get overridden, creating backup of: {' '.join(files)}")

        validate_subprocess(subprocess.run(
            backup_command,
            text=True,
            capture_output=True
        ))

        print(f"Successfully backed up files to {snapshot_name}")

    else:
        print("No files will be overridden, not creating backup")


def download_file(file_name: str, url: str) -> None:
    """Attempt to download a file or exit"""

    try:
        print(f"Attempting to download {url}")
        urllib.request.urlretrieve(url, file_name)
        print(f"Success, downloaded to {file_name}")
    except urllib.request.HTTPError as ex:
        print(f"Error occurred, does {url} exist?\n{ex}")
        sys.exit(-1)
