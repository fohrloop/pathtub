import sys
from pathlib import Path


def make_unique(items):
    # make list items unique while preserving the order.
    if sys.version_info >= (3, 6):
        f = dict
    else:  # Back in the days the python dicts were not ordered.
        from collections import OrderedDict
        f = OrderedDict
    return list(f.fromkeys(items))


def get_nonexisting_folders(folders):

    nonexisting = set()
    for folder in folders:
        if not folder:  #empty string
            continue
        f = Path(folder)
        try:
            exists = f.exists()
        except PermissionError:
            # Do not remove any folders that
            # might exist inside folder with
            # restricted access!
            continue
        if not exists:
            nonexisting |= {folder}
    return nonexisting
