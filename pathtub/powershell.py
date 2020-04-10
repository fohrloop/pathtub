import subprocess
from subprocess import check_output
import tempfile
from pathlib import Path


def run_powershell(command):
    """
    Run command in powershell and return the
    value.

    Parameters
    ---------
    command: str
        The command to run. Must not have any
        double quotes (").
    """
    if '"' in command:
        raise ValueError('command must not have double quotes!')
    command_quoted = f'"{command}"'
    full_command = f'powershell -command {command_quoted}'
    o = check_output(full_command)
    out = o.decode('utf-8').strip()
    return out
