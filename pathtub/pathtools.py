import logging
import os
from pathlib import Path
from subprocess import CalledProcessError

from pathtub.powershell import run_powershell
from pathtub.utils import make_unique, get_nonexisting_folders

logger = logging.getLogger(__name__)


class PathEditException(Exception):
    pass


def ensure(item, permanent=False, permanent_mode='user', force=False):
    """
    Ensure that an item (folder) is if PATH
    variable. If `item` is found in the Process 
    (temporary) PATH, does nothing.

    If `item` is not found in the Process PATH,
    adds to the process PATH. If you want to save
    permanently, see the `permanent` and `permanent_mode`
    flags.
    
    Safe to call every time your script starts.

    Parameters
    ----------
    item: str
        The item (folder) to be ensured to be found
        in the PATH. Duplicates will not be added.
        Last backslash is not taken into account when 
        comparing for duplicates.
    permanent: bool
        If `item` is not found in the *Process* PATH, 
        and `permanent` is True, then in addition of 
        adding the `item` to the Process PATH, the `item`
        is added permanently. Defaults to False.
    permanent_mode: 'user' (default) |'machine'
        Tells where to add the new PATH item. User means
        for "current User" and machine means "Local machine"/
        System/all users. Note that you will need Admin rights
        to use the 'machine' permanent_mode.
    force: bool
        If True, will add to the permanent PATH regardless
        if the value is found in the Process PATH or not.
        This call will take a lot longer and is not
        recommended to call always with `force`.

    Returns
    -------
    added: bool
        True, if `item` was added to PATH. False, if it was
        already in (process) PATH and was not added.


    Notes
    -----
    Here is how the PATH variables are inherited & copied:

    User PATH      Machine/System PATH 
            \                  / 
             \                / 
              v              v  
    +-----------------------------------------------------+
    | MainProcess                                         |
    |                                                     |
    |  PATH = Process PATH                                |
    |    (initially copy of User and Machine PATH)        |
    |                                                     |
    +-----------------------------------------------------+
                        |                                  
                        |                                  
                        v                                  
    +-----------------------------------------------------+
    | ChildProcess                                        |
    |                                                     |
    |   PATH = Process PATH                               |
    |     (initially copy of MainProcess PATH)            |
    +-----------------------------------------------------+
                                       
    """
    found, path = is_in_path_return_path(item, 'process')
    if found and not force:
        return False

    if not found:
        new_path = path + ';' + item

    set_process = _get_set_function('process')
    set_process(new_path)

    if permanent:
        set_permanent = _get_set_function(permanent_mode)
        set_permanent(new_path)

    return True


def get_path(mode='process'):
    """
    Get the Windows PATH variable.
    
    Parameters
    ----------
    mode: 'process' | 'user' | 'machine'
        process: The Path variable of the process
        user: Return only User Path variable
        machine: return only Machine Path variable
    """
    if mode == 'process':
        return os.environ.get('PATH', '')
    elif mode == 'user':
        command = "[Environment]::GetEnvironmentVariable('Path', 'User')"
    elif mode == 'machine':
        command = "[Environment]::GetEnvironmentVariable('Path', 'Machine')"
    else:
        raise ValueError('mode must be one of ("process", "user", "machine")')
    return run_powershell(command).strip()


def _remove(path, remove_these, path_type='User', reason='non-existing'):
    path_new = []
    for item in path:
        if item in remove_these:
            logger.warning('Removing folder %s from %s Path (%s)', item,
                           path_type, reason)
            continue
        path_new.append(item)
    return path_new


def _remove_user_machine(path_user,
                         path_machine,
                         remove_these,
                         reason='non-existing'):
    path_user = _remove(path_user,
                        remove_these,
                        path_type='User',
                        reason=reason)
    path_machine = _remove(path_machine,
                           remove_these,
                           path_type='System',
                           reason=reason)
    return path_user, path_machine


def path_string_to_list(path_str):
    path = []
    for x in path_str.strip().split(';'):
        if not x:
            continue
        if x.endswith('\\'):
            path.append(x[:-1])
            continue
        path.append(x)
    return path


def clean(sort=True, remove_non_existent=True, remove_user_duplicates=True):
    """
    Cleans the User & System PATH variables.
     * Removing duplicates from the PATH
     * Removing empty entries from PATH
     * Sorting alphabetically (optional)
     * Removing folders that do not exist (optional)
     * Removing from "User" list the ones that are in the 
       "System" list (optional)

    Parameters
    ----------
    sort: bool
        If True, sorts the Path items in the Path (User & System)
        alphabetically. If ran without admin rights, then updating 
        the System Path will be skipped. Defaults to True.
    remove_non_existent: bool
        If True, checks if the items in that PATH (User & System)
        exist in the filesystem. All paths that do not exist will
        be removed. If ran without Admin rights, then updating
        the System Path will be skipped. Defaults to True.
    remove_user_duplicates: bool
        If True, any item in the User Path that is also in the
        System Path will be removed from the User Path.
    
    """
    # Remove empty entries & remove trailing backslash
    path_user = path_string_to_list(get_path('user'))
    path_machine = path_string_to_list(get_path('machine'))

    # remove duplicates
    path_user = make_unique(path_user)
    path_machine = make_unique(path_machine)

    set_user = set(path_user)
    set_machine = set(path_machine)

    if remove_non_existent:
        nonexisting = get_nonexisting_folders(folders=set_user | set_machine)
        path_user, path_machine = _remove_user_machine(
            path_user,
            path_machine,
            nonexisting,
            reason='non-existing',
        )

    if remove_user_duplicates:
        # items that are in both, the User and System PATHS
        dups = set_user.intersection(set_machine)

        path_user = _remove(
            path_user,
            dups,
            path_type='User',
            reason='Defined in both; User and System PATH',
        )

    if sort:
        path_user = sorted(path_user, key=lambda x: x.lower())
        path_machine = sorted(path_machine, key=lambda x: x.lower())

    set_user_path(';'.join(path_user))
    try:
        set_machine_path(';'.join(path_machine))
    except PathEditException:
        logger.warning('Could not clean the SYSTEM PATH! Needs Admin rights!')


def set_path(path, mode='user'):

    if mode == 'both':
        set_user_path(path)
        set_machine_path(path)
    elif mode == 'user':
        set_user_path(path)
    elif mode == 'machine':
        set_machine_path(path)


def set_process_path(path):
    os.environ['PATH'] = path


def set_user_path(path):
    command = "[Environment]::SetEnvironmentVariable("
    command += f"'Path', '{path}',"
    command += "[EnvironmentVariableTarget]::User )"
    return run_powershell(command)


def set_machine_path(path):
    # This needs Admin rights!
    command = "[Environment]::SetEnvironmentVariable("
    command += f"'Path', '{path}',"
    command += "[EnvironmentVariableTarget]::Machine )"
    try:
        return run_powershell(command)
    except CalledProcessError:
        raise PathEditException(
            f'Could not set PATH (Machine)! Make sure you run the script with Admin rights '
        )


def _get_set_function(mode):

    if mode == 'process':
        f = set_process_path
    elif mode == 'user':
        f = set_user_path
    elif mode == 'machine':
        f = set_machine_path
    else:
        raise ValueError('mode must be one of ("process", "user", "machine")')
    return f


def add_to_path(item, mode='process'):
    """
    Add a folder to the Windows PATH variable
    (Process, User or Machine). Only adds to the PATH
    if it is not in the PATH already (safe to
    call multiple times with same `item`).
    
    Parameters
    ----------
    item: str
        The folder to add to the PATH
    mode: 'process' (default) | 'user' | 'machine'
        process: add to 'Process' PATH (temporary)
        user: add to 'User' PATH (permanent)
        machine: add to 'Machine' PATH (permanent)

    Returns
    -------
    added: bool
        True, if added `item` to PATH.
        False, if the `item` was already
        in the PATH (no need to add).

    NOTE: Adding to 'machine' PATH needs
         Administrative rights (elevated shell)!
    """

    found, path = is_in_path_return_path(item, mode)

    if found:  # do not add duplicates.
        return False

    f = _get_set_function(mode)

    new_path = path + ';' + item
    f(new_path)
    return True


def remove_from_path(item, mode='process'):
    """
    Remove a folder from the Windows PATH variable
    (User or Machine).

    Parameters
    ----------
    item: str
        The folder remove from the PATH
    mode: 'process' | 'user' | 'machine'
        process: Remove from 'Process' PATH (temporary)
        user: Remove from 'User' PATH (permanent)
        machine: Remove from 'Machine' PATH (permanent)

    Returns
    -------
    done: bool
        False, if the `item` was not found in the
        PATH and PATH is unaltered
        True, if the `item` was found and removed
        from the PATH. 

    Raises
    ------
        If the removal was not succesful, raises
        PathEditException.
    
    NOTE: Removing from 'machine' PATH needs
         Administrative rights (elevated shell)!
    """

    found, path = is_in_path_return_path(item, mode)
    if not found:
        return False

    f = _get_set_function(mode)

    paths = path.strip().split(';')
    paths.pop(paths.index(item))
    # sometimes there are "empty" entries (;;) in the PATH: remove these, too.
    new_path = ';'.join([p for p in paths if p])
    f(new_path)
    return True


def is_in_path_return_path(item, mode='process'):
    r"""
    Check whether an `item` is in Path (Process 
    Path, User Path or Machine Path). Also returns 
    the `path`.

    Parameters
    ----------
    item: str
        The folder to check against. The
        last backslash, if any, is neglected
        (user does not have to worry if the folder
        in PATH has backslash or not in the end.)
    mode: 'process' | 'user' | 'machine'
        user: Return only User Path variable
        machine: return only Machine Path variable


    Returns
    -------

    found, path: (bool, str)
        found: True, if the `item` is in the "Path". 
          False otherwise.
        path: the path as string.   
    """
    if item.endswith('\\'):
        item = item[:-1]
    path = get_path(mode)
    paths = {x[:-1] if x.endswith('\\') else x for x in path.split(';')}

    found = item in paths

    return found, path


def is_in_path(item, mode='process'):
    r"""
    Check whether an `item` is in Path 
    (Process Path, User Path or Machine Path). 

    Parameters
    ----------
    item: str
        The folder to check against. The
        last backslash, if any, is neglected
        (user does not have to worry if the folder
        in PATH has backslash or not in the end.)
    mode: 'process' | 'user' | 'machine'
        user: Return only User Path variable
        machine: return only Machine Path variable

    Returns
    -------

    found: bool
        True, if the `item` is in the "Path". 
        False otherwise.   
    """
    found, path = is_in_path_return_path(item, mode)

    return found