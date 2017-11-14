__version__ = "0.1"

class myError(Exception):
    def _get_message(self): 
        return self._message
    def _set_message(self, message): 
        self._message = message
    message = property(_get_message, _set_message)
 
#def set_lib_package_path():
#    import sys, os
#    sys.path.append(os.path.dirname(sys.argv[0]) + "/..")

#try:
#    import lib
#except:
#    set_lib_package_path()

#import lib

__all__ = [
    # - Package symbols (i.e. defined into this file)
    "iceraError",


    # - Package modules (i.e. files named *.py contained into this package directory)
    "attribute",
    "superTypes",
    

    # - Sub-packages (i.e. sub-directories containing other packages)
]

if __name__ == "__main__":
    version = """
Version library: %s
""" % (__version__,)
    print version

