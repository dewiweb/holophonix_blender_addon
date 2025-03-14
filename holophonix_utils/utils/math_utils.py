import numpy
from numpy import radians
from typing import Union, Tuple


# ------------------------------
# Coordinate Conversion
# ------------------------------

def cart2sph(z: Union[float, numpy.ndarray], y: Union[float, numpy.ndarray], x: Union[float, numpy.ndarray]) -> numpy.ndarray:
    """
    Convert Cartesian coordinates (x,y,z) to spherical coordinates (elevation, azimuth, radius).

    Args:
        z: Z coordinate or array of Z coordinates
        y: Y coordinate or array of Y coordinates
        x: X coordinate or array of X coordinates

    Returns:
        numpy.ndarray: Array containing elevation, azimuth, and radius in degrees

    Example:
        >>> cart2sph(1, 1, 1)
        array([ 35.26438968,  45.        ,   1.73205081])
    """
    try:
        radius = numpy.sqrt(x**2 + y**2 + z**2)
        azimuth = numpy.arctan2(y, x)
        elevation = numpy.arctan2(z, numpy.sqrt(x**2 + y**2))
        
        # Convert to degrees
        azimuth *= 180.0 / numpy.pi
        elevation *= 180.0 / numpy.pi
        
        return numpy.array([elevation, azimuth, radius])
    except Exception as e:
        print(f"Error in cart2sph conversion: {str(e)}")
        raise


def sph2cart(*args: Union[numpy.ndarray, float]) -> Union[numpy.ndarray, Tuple[float, float, float]]:
    """
    Convert spherical coordinates (elevation, azimuth, radius) to Cartesian coordinates (x,y,z).

    Args:
        *args: Either a single Nx3 array or three separate values (elevation, azimuth, radius)

    Returns:
        Union[numpy.ndarray, Tuple[float, float, float]]: Cartesian coordinates as array or tuple

    Example:
        >>> sph2cart(45, 45, 1)
        (0.5, 0.5, 0.7071067811865475)
    """
    try:
        if len(args) == 1:  # Nx3 array
            elev = args[0][0, :]
            azim = args[0][1, :]
            radius = args[0][2, :]
            return_as_array = True
        elif len(args) == 3:  # Separate values
            elev, azim, radius = args
            return_as_array = False
        else:
            raise ValueError("Invalid number of arguments. Expected 1 (Nx3 array) or 3 (elev, azim, radius)")

        z = radius * numpy.sin(radians(elev))
        x = radius * numpy.cos(radians(elev)) * numpy.cos(radians(azim))
        y = radius * numpy.cos(radians(elev)) * numpy.sin(radians(azim))

        return numpy.asarray([x, y, z]) if return_as_array else (y, x, z)
    except Exception as e:
        print(f"Error in sph2cart conversion: {str(e)}")
        raise
