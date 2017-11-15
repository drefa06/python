#!/usr/bin/env python

__version__ = "0.1"

def set_lib_package_path():
    import sys, os
    sys.path.append(os.path.dirname(sys.argv[0]) + "/..")
    sys.path.append(sys.path.pop(0))


set_lib_package_path()

import lib

##
# @brief Package public symbols list
#
# @details
# @see
# @li The top level package lib : Packages common documentation / Packages public symbols list
# 
__all__ = [
    # - Package symbols (i.e. defined into this file)
    # None

    # - Package modules (i.e. files named *.py contained into this package directory)

    # - Sub-packages (i.e. sub-directories containing other packages)
    "lib",
]

if __name__ == "__main__":
    version = """
Version moduletest: %s
""" % (__version__,)
    print version


