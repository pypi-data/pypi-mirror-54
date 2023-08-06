#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""check sub-module

This module handles logging options and verbose levels.

"""

import os
import psutil
import shutil
from pycif.utils import path

import logging


def init_log(logfile, workdir, loglevel):
    """Initializes the log file for verbose outputs.

    Args:
        logfile (str): log file name
        workdir (str): directory where to create the logfile
        loglevel (int): level of verbosity.
                        2 for debug level, 1 for standard outputs

    Returns:
        (str, str) : (full path to the log file,
                      absolute path to the working directory)

    Notes: Beware that the function overwrites any existing log file.
    """
    
    # Turning the path to absolute and creating the directory
    workdir, _ = path.init_dir(workdir)
    
    if not os.path.isabs(logfile):
        logfile = "{}/{}".format(workdir, logfile)
    
    # Beware that the log_file is over-writen anyway
    open(logfile, 'w').close()
    
    level = logging.DEBUG
    if loglevel <= 1:
        level = logging.INFO
    
    logging.basicConfig(format='%(message)s',
                        filename=logfile, level=level)
    
    return logfile, workdir


def verbose(entry, logfile=None):
    """Prints out a log entry to the log_file
    
    Args:
        entry (string): entry to print
        logfile (file path): path to the log file

    Returns:
        None

    """
    
    print entry
    
    if logfile is not None:
        with open(logfile, 'a') as f:
            f.write(entry + '\n')
    
    else:
        logging.info(entry)


def check_memory(logfile=None):
    verbose("Current memory usage: {} Mb"
            .format(psutil.Process(os.getpid()).memory_info()[0]
                    / float(2 ** 20)),
            logfile)
