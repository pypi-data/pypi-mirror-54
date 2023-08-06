import os
from types import MethodType

from pycif.utils import path
from pycif.utils.check import verbose

from read import read
from write import write

requirements = {'domain': {'name': 'LMDZ', 'version': 'std', 'empty': False}}
