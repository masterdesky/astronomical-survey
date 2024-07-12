#
#
#
#
#

import numpy as np
from _utils import *
from constants import J2000, dS


def gd2jd(Y, M, D, UT=0):
    '''
    Converts a Gregorian UTC datetime to Julian Date.

    Parameters:
    -----------
    Y : int
        Gregorian year.
    M : int
        Gregorian month.
    D : int
        Gregorian day.
    UT : float, optional
        Time in UTC, default value corresponds to 00:00 UTC.

    Returns:
    --------
    JD : float
    '''
    JDN = 367 * Y - 7 * (Y + (M + 9) // 12) // 4 + 275 * M // 9 + D - 730531.5
    JDN += J2000
    f = UT / 24  # Fraction of the day
    return JDN + f


def gmst(Y, M, D):
    '''
    Calculates the Greenwich Mean Sidereal Time (GMST = S0) on a given
    date at 00:00 UTC.

    Parameters:
    -----------
    Y : int
        Gregorian year.
    M : int
        Gregorian month.
    D : int
        Gregorian day.

    Returns:
    --------
    GMST : float
        Greenwhich Mean Sidereal Time in hours.
    '''
    JD = gd2jd(Y=Y, M=M, D=D, UT=0)
    T_u = (JD - J2000) / 36525  # Number of Julian centuries since J2000

    c0, c1, c2, c3 = 24110.54841, 8640184.812866, 0.093104, 6.2e-05
    GMST = (c0 + c1 * T_u + c2 * T_u**2 - c3 * T_u**3) / 3600 % 24  # Hours
    return GMST


def lmst(Y, M, D, UT=0, long=0):
    '''
    Calculates Local Mean Sidereal Time (LMST = S) on the given date and
    time at a specific location.

    Parameters:
    -----------
    Y : int
        Gregorian year.
    M : int
        Gregorian month.
    D : int
        Gregorian day.
    UT : float, optional
        Time in UTC hours, default value corresponds to 00:00 UTC.
    long : float, optional
        The longitude in degrees of the location the LMST is calculated
        for.

    Returns:
    --------
    LMST : float
        Local Mean Sidereal Time in hours.
    '''
    # Normalize input parameters to their expected ranges
    long = normalize_asym(x=long, p=180)

    GMST = gmst(Y, M, D)
    LMST = GMST + long/15 + dS * UT
    return LMST