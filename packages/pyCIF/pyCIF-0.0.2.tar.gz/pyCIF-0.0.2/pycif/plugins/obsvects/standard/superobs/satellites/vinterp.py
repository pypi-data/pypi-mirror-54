import numpy as np
import scipy


def vertical_interp(pres_in, pres_out):
    """Compute the interpolation coefficients to apply
    a linear vertical interpolation"""


    nvertin, lenin = pres_in.shape
    nvertout, lenout = pres_out.shape

    if lenin != lenout:
        raise Exception("The input mesh has a different length than the target")

    # Initializing index mesh for scipy.griddata
    meshin = np.array((nvertin + 2)
                      * [range(lenin)])
    meshout = np.array(nvertout * [range(lenout)])

    levmeshin = np.array((lenin)
                         * [range(-1, nvertin + 1)]).T
    levin = levmeshin.flatten()

    # Initializing pressure mesh for scipy.griddata
    # For input pressures (those of the model),
    # extending the roof and floor to detect ak points
    # outside of the hull of model pressures
    pin = np.concatenate(
        [pres_in.max() * np.ones((1, lenin)) + 1, pres_in,
         pres_in.min() * np.ones((1, lenout)) - 1], axis=0).flatten()
    pout = pres_out.flatten()

    # Aggegating points in scipy.griddata format
    points_in = np.array([meshin.flatten(), pin]).T
    points_out = np.array([meshout.flatten(), pout]).T

    # Retrieving location of ak levels versus model levels
    levout = scipy.interpolate.griddata(
        points_in, levin, points_out).reshape((-1, lenout))

    # Getting interpolation coefficients
    xlow = np.floor(levout).astype(int)
    xhigh = xlow + 1

    alphalow = levout - xlow
    alphahigh = 1 - alphalow

    # Cropping ak pressure outside of model pressures
    toolow = xlow <= 0
    toohigh = xhigh >= nvertin - 1

    xlow[toolow] = 0
    xhigh[toohigh] = nvertin - 1

    alphalow[toolow] = 1
    alphahigh[toolow] = 0
    alphalow[toohigh] = 0
    alphahigh[toohigh] = 1

    return xlow, xhigh, alphalow, alphahigh
