from pathtub.powershell import run_powershell
from subprocess import CalledProcessError


class PathEditException(Exception):
    pass


def get_path(mode='path'):
    """
    Get the Windows PATH variable.
    Note: contains the User and Machine wide
        Path variables added together.
    
    Parameters
    ----------
    mode: 'path' | 'user' | 'machine'
        user: Return only User Path variable
        machine: return only Machine Path variable
        path: Return the combined value ($Env:Path
         in powershell or PATH in cmd). NOTE: This
         is *not* in every situation the same as the
         union of 'user' and 'machine'.
    """
    if mode == 'path':
        command = "$Env:Path"
    elif mode == 'user':
        command = "[Environment]::GetEnvironmentVariable('Path', 'User')"
    elif mode == 'machine':
        command = "[Environment]::GetEnvironmentVariable('Path', 'Machine')"
    else:
        raise ValueError('mode must be one of ("user", "machine", "path")')
    return run_powershell(command).strip()


def set_path(path, mode='user'):

    if mode == 'both':
        set_user_path(path)
        set_machine_path(path)
    elif mode == 'user':
        set_user_path(path)
    elif mode == 'machine':
        set_machine_path(path)


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


def add_to_path(item, mode='user'):
    """
    Add a folder to the Windows PATH variable
    (User or Machine). Only adds to the PATH
    if it is not in the PATH already (safe to
    call multiple times with same `item`).
    
    Parameters
    ----------
    item: str
        The folder to add to the PATH
    mode: 'user' (default) | 'machine'
        user: add to 'User' PATH
        machine: add to 'Machine' PATH

    Returns
    -------
    added: bool
        True, if added `item` to PATH.
        False, if the `item` was already
        in the PATH (no need to add).

    NOTE: Adding to 'machine' PATH needs
         Administrative rights (elevated shell)!
    """

    path = get_path(mode)
    if item in path:
        return False
    if mode == 'user':
        f = set_user_path
    elif mode == 'machine':
        f = set_machine_path
    else:
        raise ValueError('mode must be one of ("user", "machine")')

    new_path = path + ';' + item
    f(new_path)
    return True


def remove_from_path(item, mode='user'):
    """
    Remove a folder from the Windows PATH variable
    (User or Machine).

    Parameters
    ----------
    item: str
        The folder remove from the PATH
    mode: 'user' (default) | 'machine'
        user: Remove from 'User' PATH
        machine: Remove from 'Machine' PATH

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

    path = get_path(mode)
    if item not in path:
        return False

    if mode == 'user':
        f = set_user_path
    elif mode == 'machine':
        f = set_machine_path
    else:
        raise ValueError('mode must be one of ("user", "machine")')

    paths = path.strip().split(';')
    paths.pop(paths.index(item))
    # sometimes there are "empty" entries (;;) in the PATH: remove these, too.
    new_path = ';'.join([p for p in paths if p])
    f(new_path)
    return True


def is_in_path(item, mode='path'):
    r"""
    Check whether an `item` is 
    in Path (PATH, User Path or Machine
    Path). 

    Parameters
    ----------
    item: str
        The folder to check against. The
        last backslash, if any, is neglected
        (user does not have to worry if the folder
        in PATH has backslash or not in the end.)
    mode: 'path' | 'user' | 'machine'
        user: Return only User Path variable
        machine: return only Machine Path variable
        path: Return the combined value ($Env:Path
         in powershell or PATH in cmd). NOTE: This
         is *not* in every situation the same as the
         union of 'user' and 'machine'.

    Returns
    -------
    found: bool
        True, if the `item` is in the "Path". 
        False otherwise.   
    """
    if item.endswith('\\'):
        item = item[:-1]
    path = get_path(mode)
    paths = [x[:-1] if x.endswith('\\') else x for x in path.split(';')]

    return item in paths