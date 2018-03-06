# -*- coding: utf-8 -*-

__all__ = [
    # - Package symbols (i.e. defined into this file)
    "set_lib_package_path",

    # - Package modules (i.e. files named *.py contained into this package directory)
    "test_ip",
    "test_inputNonBlocking",
    "test_robot",
    "test_cartes",

    # - Sub-packages (i.e. sub-directories containing other packages)
]

def set_lib_package_path():
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),"..","..")))


try:
    import lib
except:
    set_lib_package_path()
    import lib