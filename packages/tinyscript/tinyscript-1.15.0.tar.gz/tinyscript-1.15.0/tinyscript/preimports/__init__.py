# -*- coding: UTF-8 -*-
"""Module for defining the list of preimports.

"""
from importlib import import_module
try:  # will work in Python 3
    from importlib import reload
except ImportError:  # will fail in Python 2 ; it will keep the built-in reload
    reload = reload

from .hash import hashlib
from .venv import virtualenv, VirtualEnv


__all__ = __features__ = ["hashlib", "virtualenv", "VirtualEnv"]
__all__ += ["__badimports__", "__optimports__", "__preimports__",
            "load", "reload"]

__badimports__ = []
__optimports__ = [
    "fs",
    "numpy",
    "pandas",
]
__preimports__ = [
    "argparse",
    "ast",
    "base64",
    "binascii",
    "codecs",
    "collections",
    "fileinput",
    "itertools",
    "logging",
    "os",
    "random",
    "re",
    "shutil",
    "signal",
    "string",
    "subprocess",
    "sys",
    "time",
]


def _load_preimports(*extras):
    """
    This loads the list of modules to be preimported in the global scope.
    
    :param extra: additional modules
    :return:      list of successfully imported modules, list of failures
    """
    for module in __preimports__ + list(extras):
        load(module)
    for module in __optimports__:
        load(module, True)


def load(module, optional=False):
    """
    This loads a module and, in case of failure, appends it to a list of bad
     imports or not if it is required or optional.
    
    :param module:   module name
    :param optional: whether the module is optional or not
    """
    global __badimports__, __features__, __preimports__
    try:
        globals()[module] = m = import_module(module)
        m.__name__ = module
        __features__.append(module)
        return m
    except ImportError:
        if not optional and module not in __badimports__:
            __badimports__.append(module)


_load_preimports()
__preimports__ += ["hashlib", "virtualenv"]
