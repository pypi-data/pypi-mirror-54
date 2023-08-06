from .execute import execute
from types import MethodType
import pycif.utils.dates as dates

requirements = {'obsvect': {'any': True, 'empty': False,
                            'name': 'standard', 'version': 'std'},
                'controlvect': {'any': True, 'empty': False,
                                'name': 'standard', 'version': 'std'},
                'obsoperator': {'any': True, 'empty': True,
                                'name': 'standard', 'version': 'std'},
                }
