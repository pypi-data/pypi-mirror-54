import os
from types import MethodType

from pycif.utils import path
from pycif.utils.check import verbose

from read import read
from write import write
from make import make

requirements = {'domain': {'name': 'dummy', 'version': 'std', 'empty': False}}
