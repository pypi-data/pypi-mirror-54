#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import glob

setup(
    name='pyCIF',
    version='0.0.2',
    description=(
        'A Python-based interface to the Community Inversion Framework'
    ),
    packages=find_packages(),
    scripts=glob.glob('bin/*.sh'),
    install_requires=[
        'numpy',
        'scipy<=1.2',
        'matplotlib<3',
        'pandas',
        'netCDF4',
        'pytz',
        'python-dateutil',
        'xarray<=0.11',
        'pyyaml',
        'pyproj',
        'psutil',
        'Pillow<7'
    ],
    extras_require={
        'dev': [
            'Sphinx',
            'sphinx_rtd_theme',
            'sphinxcontrib-napoleon'
        ]
    },
    python_requires='>=2.7,<3'
)
