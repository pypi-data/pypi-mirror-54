def create_domain(domain,
                  **kwargs):
    """Creates a grid if needed

    Args:
        domain (dictionary): dictionary defining the domain.

    Returns:
         Error as LMDZ shouldn't be used with unknown grids

    """
    
    logfile = kwargs.get('logfile', None)
    
    check.verbose("TO DO", logfile)
    
    raise Exception
