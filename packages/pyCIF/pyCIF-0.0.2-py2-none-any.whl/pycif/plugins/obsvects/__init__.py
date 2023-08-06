from os.path import dirname, basename, isdir
import glob

modules = glob.glob(dirname(__file__) + "/*")

__all__ = [basename(f) for f in modules
           if isdir(f) and not f.endswith('.py')]

import register
