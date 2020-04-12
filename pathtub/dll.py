"""
This module defines functions that should be used to 
add or remove dll folders to be visible for python

Important functions
-------------------
- ensure_dll
- forget_dll
"""

from enum import Flag, auto
import os
import sys
import logging

from pathtub.pathtools import ensure, remove_from_path

logger = logging.getLogger(__name__)


class DllItemType(Flag):
    NoneType = 0
    Path = auto()
    AddedDllDirectory = auto()


class DllItem:
    def __init__(self, dll_folder):
        """
        Parameters
        ---------
        dll_folder: str
            The DLL folder
        """

        self.dll_folder = dll_folder
        self.itemtype = DllItemType.NoneType
        self.dll_dir_handle = None

        if sys.version_info >= (3, 8):
            # In Python 3.8+, the PATH and cwd are
            # NOT checked for DLLs
            # https://docs.python.org/3.8/whatsnew/3.8.html#bpo-36085-whatsnew

            # https://docs.python.org/3.8/library/os.html#os.add_dll_directory
            self.dll_dir_handle = os.add_dll_directory(dll_folder)
            self.itemtype |= DllItemType.AddedDllDirectory
            # For some cases, adding with `os.add_dll_directory` is not enough!
            # See, for example: https://github.com/np-8/pathtub/issues/2
            ensure(self.dll_folder, permanent=False)
            self.itemtype |= DllItemType.Path
        else:
            # In Python <3.8 there is no os.add_dll_directory
            ensure(self.dll_folder, permanent=False)
            self.itemtype |= DllItemType.Path

    def remove(self):

        if bool(self.itemtype & DllItemType.AddedDllDirectory):
            self.dll_dir_handle.close()
        if bool(self.itemtype & DllItemType.Path):
            remove_from_path(self.dll_folder, mode='process')


class DllPathContainer:
    def __init__(self):
        # container for added dirs
        # keys: folders (strings)
        # values: DllItem
        self.dll_items = dict()

    def add(self, dll_directory):
        """
        Parameters
        ---------
        dll_directory: str
            The dll directory containing 
            DLL's that should be visible to 
            Python DLL's loaded by Python.
        """
        if dll_directory in self.dll_items:
            logger.warning('%s already added. Skipping.', dll_directory)
            return
        self.dll_items[dll_directory] = DllItem(dll_directory)

    def remove(self, dll_directory):
        """
        Parameters
        ---------
        dll_directory: str
            The dll directory containing 
            DLL's that should be visible to 
            Python DLL's loaded by Python.
        """
        try:
            item = self.dll_items.pop(dll_directory)
        except KeyError:
            return
        item.remove()


# This is a container for DLL paths added during runtime
DLL_PATHS = DllPathContainer()


def ensure_dll(dll_directory):
    """
    Ensures that python and Windows can find DLL's
    specified in a dll_directory.

    Parameters
    ---------
    dll_directory: str
        The dll directory containing 
        DLL's that should be visible to 
        Python DLL's loaded by Python.
    """
    global DLL_PATHS

    DLL_PATHS.add(dll_directory)


def forget_dll(dll_directory):
    """
    Forgets a dll_directory added with 
    ensure_dll.

    Parameters
    ---------
    dll_directory: str
        The dll directory
    """
    global DLL_PATHS

    DLL_PATHS.remove(dll_directory)
