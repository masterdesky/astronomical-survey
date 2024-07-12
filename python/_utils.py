#
#
#
#
#

import numpy as np


def normalize_asym(x, p):
    '''
    Normalize a value to the inverval of :math:`[-p, p]` on a meridian.
    Normalized values from :math:`0 \to p` are equivalent to the values
    in the interval :math:`2p \to p` times :math:`-1`.

    Parameters:
    -----------
    x : float
        Value to normalize.
    p : float
        Edge of the interval.

    Returns:
    --------
    xn : float
        Normalized value.
    '''
    assert p > 0, 'The value of `p` cannot be non-positive!'
    xn = (x + p) % (2*p) - p
    return xn


def normalize_sym(x, p):
    '''
    Normalize a value to the inverval of :math:`[-p, p]` on a meridian.
    Normalized values from :math:`2p \to p` are equivalent to
    :math:`0 \to p`. Similarly, values from :math:`-2p \to -p` are
    equivalent to :math:`0 \to -p`.

    Parameters:
    -----------
    x : float
        Value to normalize.
    p : float
        Edge of the symmetric interval.

    Returns:
    --------
    xn : float
        Normalized value.
    '''
    assert p > 0, 'The value of `p` cannot be non-positive!'
    xn = normalize_asym(x, 2*p)  # First normalize to [-2p, 2p]
    xn = np.sign(xn)*(2*p) - xn if np.abs(xn) > p else xn
    return xn


def normalize_cyc(x, p):
    assert p > 0, 'The value of `p` cannot be non-positive!'
    return x%p, x//p