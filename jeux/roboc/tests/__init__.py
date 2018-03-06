# -*- coding: utf-8 -*-
__version__ = "0.1"

__all__ = [
    # - Package symbols (i.e. defined into this file)
    "set_lib_package_path",

    # - Package modules (i.e. files named *.py contained into this package directory)
    #

    # - Sub-packages (i.e. sub-directories containing other packages)
    "lib",
    "elements",
]

def set_lib_package_path():
    import sys, os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),'..')))
    sys.path.append(sys.path.pop(0))

try:
    import lib
except:
    set_lib_package_path()
    import lib


if __name__ == "__main__":
    version = """
Version tests: %s
""" % (__version__,)
    print(version)

