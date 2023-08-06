import numpy as np
from osgeo import gdal, ogr, osr


def dist_matrix(zlat, zlon, projection='gps'):
    """Computes the distance matrix for two arrays of longitudes and
    latitudes
    
    Args:
        zlat (np.array): numpy array of latitudes
        zlon (np.array): numpy array of longitudes
        projection (str): the projection used for the longitudes and latitudes
    
    Returns:
        np.array((zlat.size, zlat.size)): matrix of distances
    
    """
    
    if zlat.size != zlon.size:
        raise ValueError("Warning: longitudes and latitudes do not have the "
                         "same dimension. Cannot compute the distance matrix")
    
    # Dealing differently with gps and xy projections
    if projection == 'gps':
        # Earth radius
        rearth = 6371.03
        
        # Flatten lon/lat
        radlat = np.radians(zlat).flatten()
        radlon = np.radians(zlon).flatten()
        
        # Compute the distance
        val = (1 - np.sin(radlat[:, np.newaxis]) * np.sin(radlat[np.newaxis, :])
               - np.cos(radlat[:, np.newaxis]) * np.cos(radlat[np.newaxis, :])
               * np.cos(radlon[:, np.newaxis] - radlon[np.newaxis, :])) / 2
        val[val < 0] = 0
        
        dx = rearth * 2 * np.arcsin(val ** 0.5)
    
    elif projection == 'xy':
        lat = zlat.flatten()
        lon = zlon.flatten()
        
        dlat = (lat[:, np.newaxis] - lat[np.newaxis, :]) ** 2
        dlon = (lon[:, np.newaxis] - lon[np.newaxis, :]) ** 2
        dx = dlat + dlon
        dx = np.sqrt(dx)
    
    else:
        raise ValueError("Projection {} is not recognized".format(projection))
    
    return dx


def calc_areas(domain, **kwargs):
    """Compute grid cells surfaces

    Args:
        domain (Plugin): a domain dictionary with pre-loaded zlonc and zlatc
        **kwargs (dictionary): any extra arguments

    Returns:
        numpy.array with all areas in m2

    """
    
    # Reference GPS projection
    srsQuery = osr.SpatialReference()
    srsQuery.ImportFromEPSG(4326)
    
    # Grid corners
    zlonc = domain.zlonc
    zlatc = domain.zlatc
    nmerid = domain.nlat
    nzonal = domain.nlon
    
    # Loop over all cells
    areas = np.array(
        [[calc_cellarea(i, j, zlonc, zlatc, srsQuery)
          for j in range(nzonal)]
         for i in range(nmerid)])
    
    domain.areas = areas


def calc_cellarea(i, j, zlonc, zlatc, srsQuery):
    # Create ring
    ring = ogr.Geometry(ogr.wkbLinearRing)
    _ = ring.AddPoint(zlonc[i, j], zlatc[i, j])
    _ = ring.AddPoint(zlonc[i + 1, j], zlatc[i + 1, j])
    _ = ring.AddPoint(zlonc[i + 1, j + 1], zlatc[i + 1, j + 1])
    _ = ring.AddPoint(zlonc[i, j + 1], zlatc[i, j + 1])
    _ = ring.AddPoint(zlonc[i, j], zlatc[i, j])

    # Define local projection
    srsArea = osr.SpatialReference()
    srsArea.ImportFromProj4(
        '+proj=laea +lat_0=80 +lon_0={} +x_0=0 +y_0=0 '
        '+ellps=WGS84 +units=m +no_defs '
            .format(zlatc[i, j], zlonc[i, j])
    )

    transf = osr.CoordinateTransformation(srsQuery, srsArea)

    ring.Transform(transf)

    # Returns area in m2
    return ring.GetArea()
