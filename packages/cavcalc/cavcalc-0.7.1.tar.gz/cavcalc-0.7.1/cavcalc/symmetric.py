import cmath
import numpy as np

from .parameter import Parameter
from .utilities import both_arraylike, modesep_adjust
from .utilities.maths import abcd

## gsingle refers to the g-factor of a single mirror of the
## cavity, gcav is the overall g-factor of the cavity where
## gcav = gsingle * gsingle
##
## note that gsingle is the g-factor of BOTH cavity mirrors
## as this file represents equations for symmetric cavities

### Beam radius relations

def w_of_gsingle(L, wl, gsingle):
    """Beam radius on symmetric cavity mirrors as function of
    the g-factor of one of the mirrors (gsingle = g1 = g2).

    Parameters
    ----------
    L : float or array like
        Length of the cavity [m].

    wl : float or array like
        Wavelength of the field [m].

    gsingle : float or array like
        Stability factor of one of the cavity mirrors (equal to
        the other mirror in this case).

    Returns
    -------
    out : float or array like
        Radius of the beam on the cavity mirrors [m].
    """
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, gsingle):
        L, gsingle = np.meshgrid(L, gsingle)
    elif both_arraylike(wl, gsingle):
        wl, gsingle = np.meshgrid(wl, gsingle)
    return np.sqrt(L * wl / np.pi * np.sqrt(1 / (1 - gsingle * gsingle)))

def w_of_gcav(L, wl, gcav):
    """Beam radius on symmetric cavity mirrors as function of
    the overall g-factor of the cavity (gcav = g1**2; where g1 = g2).

    Parameters
    ----------
    L : float or array like
        Length of the cavity [m].

    wl : float or array like
        Wavelength of the field [m].

    gcav : float or array like
        Stability factor of the cavity (gcav = g1 * g2; where g1 = g2 in this case).

    Returns
    -------
    out : float or array like
        Radius of the beam on the cavity mirrors [m].
    """
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, gcav):
        L, gcav = np.meshgrid(L, gcav)
    elif both_arraylike(wl, gcav):
        wl, gcav = np.meshgrid(wl, gcav)
    return np.sqrt(L * wl / np.pi * np.sqrt(1 / (1 - gcav)))

def w_of_rtgouy(L, wl, rtgouy):
    """Beam radius on symmetric cavity mirrors as function of
    the round-trip Gouy phase of the cavity field.

    Parameters
    ----------
    L : float or array like
        Length of the cavity [m].

    wl : float or array like
        Wavelength of the field [m].

    rtgouy : float or array like
        Round-trip Gouy phase of the cavity field [radians].

    Returns
    -------
    out : float or array like
        Radius of the beam on the cavity mirrors [m].
    """
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, rtgouy):
        L, rtgouy = np.meshgrid(L, rtgouy)
    elif both_arraylike(wl, rtgouy):
        wl, rtgouy = np.meshgrid(wl, rtgouy)
    return np.sqrt(L * wl / (np.pi * np.sin(rtgouy * 0.5)))

def w_of_divang(L, wl, theta):
    """Beam radius on symmetric cavity mirrors as function of
    the divergence angle of the cavity field.

    Parameters
    ----------
    L : float or array like
        Length of the cavity [m].

    wl : float or array like
        Wavelength of the field [m].

    theta : float or array like
        Divergence angle of the cavity field [radians].

    Returns
    -------
    out : float or array like
        Radius of the beam on the cavity mirrors [m].
    """
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, theta):
        L, theta = np.meshgrid(L, theta)
    elif both_arraylike(wl, theta):
        wl, theta = np.meshgrid(wl, theta)
    factor_L_wl = (L * np.pi / (2 * wl))**2 * np.power(np.tan(theta), 4)
    one_minus_gsqd = 1 - ((1 - factor_L_wl) / (1 + factor_L_wl))**2
    return np.sqrt(L * wl/np.pi * np.sqrt(1 / one_minus_gsqd))

def w0_of_gsingle(L, wl, gsingle):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, gsingle):
        L, gsingle = np.meshgrid(L, gsingle)
    elif both_arraylike(wl, gsingle):
        wl, gsingle = np.meshgrid(wl, gsingle)
    return np.sqrt(0.5 * L * wl / np.pi * np.sqrt((1 + gsingle) / (1 - gsingle)))

def w0_of_gcav(L, wl, gcav):
    return w0_of_gsingle(L, wl, gsingle_of_gcav(gcav))

def w0_of_rtgouy(L, wl, rtgouy):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, rtgouy):
        L, rtgouy = np.meshgrid(L, rtgouy)
    elif both_arraylike(wl, rtgouy):
        wl, rtgouy = np.meshgrid(wl, rtgouy)
    inner_sqrt_term = np.sqrt((1 + np.cos(0.5 * rtgouy))/(1 - np.cos(0.5 * rtgouy)))
    return np.sqrt(0.5 * L * wl / np.pi * inner_sqrt_term)

def z0_symmetric(L):
    return 0.5 * L

## RoC relations

def roc_of_gsingle(L, gsingle):
    if both_arraylike(L, gsingle):
        L, gsingle = np.meshgrid(L, gsingle)
    return L / (1 - gsingle)

## Stability relations

### singular

def gsingle_of_roc(L, Rc):
    if both_arraylike(L, Rc):
        L, Rc = np.meshgrid(L, Rc)
    return 1 - L/Rc

def gsingle_of_w(L, wl, w):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, w):
        L, w = np.meshgrid(L, w)
    elif both_arraylike(wl, w):
        wl, w = np.meshgrid(wl, w)
    mag = np.sqrt(1 - (L * wl / (np.pi * w * w))**2)
    return np.array([-mag, mag])

def gsingle_of_rtgouy(rtgouy):
    mag = np.cos(0.5 * rtgouy)
    # rtgouy has already been computed from upper / lower quadrants
    # so don't split it again
    # NOTE quadrant calculations will be handled better in a later version
    if isinstance(rtgouy, np.ndarray) and rtgouy.size == 2:
        return mag
    return np.array([-mag, mag])

def gsingle_of_divang(L, wl, theta):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, theta):
        L, theta = np.meshgrid(L, theta)
    elif both_arraylike(wl, theta):
        wl, theta = np.meshgrid(wl, theta)
    factor_L_wl = (L * np.pi / (2 * wl))**2 * np.power(np.tan(theta), 4)
    return (1 - factor_L_wl) / (1 + factor_L_wl)

def gsingle_of_gcav(gcav):
    mag = np.sqrt(gcav)
    return np.array([-mag, mag])

### cavity

def gcav_of_roc(L, Rc):
    return gsingle_of_roc(L, Rc)**2

def gcav_of_gsingle(gsingle):
    return gsingle * gsingle

def gcav_of_w(L, wl, w):
    return gsingle_of_w(L, wl, w)[0]**2

def gcav_of_rtgouy(rtgouy):
    return gsingle_of_rtgouy(rtgouy)[0]**2

def gcav_of_divang(L, wl, theta):
    return gsingle_of_divang(L, wl, theta)[0]**2

# Round-trip Gouy phase relations

def rtgouy_of_gsingle(gsingle):
    return 2 * np.arccos(gsingle)

def rtgouy_of_gcav(gcav):
    return rtgouy_of_gsingle(gsingle_of_gcav(gcav))

def rtgouy_of_w(L, wl, w):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, w):
        L, w = np.meshgrid(L, w)
    elif both_arraylike(wl, w):
        wl, w = np.meshgrid(wl, w)
    return 2 * np.arcsin(L * wl/(np.pi * w * w))

def rtgouy_of_divang(L, wl, theta):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, theta):
        L, theta = np.meshgrid(L, theta)
    elif both_arraylike(wl, theta):
        wl, theta = np.meshgrid(wl, theta)
    factor_L_wl = (L * np.pi / (2 * wl))**2 * np.power(np.tan(theta), 4)
    return 2 * np.arccos((1 - factor_L_wl) / (1 + factor_L_wl))

# Divergence angle relations

def divang_of_gsingle(L, wl, gsingle):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, gsingle):
        L, gsingle = np.meshgrid(L, gsingle)
    elif both_arraylike(wl, gsingle):
        wl, gsingle = np.meshgrid(wl, gsingle)
    return np.sqrt(2 * wl / (L * np.pi) * np.sqrt((1 - gsingle) / (1 + gsingle)))

def divang_of_gcav(L, wl, gcav):
    return divang_of_gsingle(L, wl, gsingle_of_gcav(gcav))

def divang_of_w(L, wl, w):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, w):
        L, w = np.meshgrid(L, w)
    elif both_arraylike(wl, w):
        wl, w = np.meshgrid(wl, w)
    factor_wl_L = 2 * wl / (L * np.pi)
    inner_sqrt_term = np.sqrt(1 - (L * wl / (np.pi * w * w))**2)
    return np.sqrt(factor_wl_L * np.sqrt((1 - inner_sqrt_term) / (1 + inner_sqrt_term)))

def divang_of_rtgouy(L, wl, rtgouy):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, rtgouy):
        L, rtgouy = np.meshgrid(L, rtgouy)
    elif both_arraylike(wl, rtgouy):
        wl, rtgouy = np.meshgrid(wl, rtgouy)

    factor_wl_L = 2 * wl / (L * np.pi)

    #if not isinstance(rtgouy, np.ndarray):
        #if rtgouy < np.pi:
        #    return np.sqrt(factor_wl_L * 1 / np.tan(0.25 * rtgouy))
        #return np.sqrt(factor_wl_L * np.tan(0.25 * rtgouy))

    nominal = np.sqrt(factor_wl_L * np.tan(0.25 * rtgouy))
    #idx_gouy_less_pi = np.where(rtgouy < np.pi)
    #if len(idx_gouy_less_pi) == 1: # 1D
    #    for idx in idx_gouy_less_pi:
    #        nominal[idx] /= np.tan(0.25 * rtgouy[idx])
    #else: # meshgrid
    #    for idx_i, idx_j in zip(idx_gouy_less_pi[0], idx_gouy_less_pi[1]):
    #        nominal[idx_i][idx_j] /= np.tan(0.25 * rtgouy[idx_i][idx_j])

    return nominal

# Mode separation frequency relations

def modesep_of_rtgouy(L, rtgouy):
    if both_arraylike(L, rtgouy):
        L, rtgouy = np.meshgrid(L, rtgouy)

    return modesep_adjust(rtgouy, L)

def modesep_of_gsingle(L, gsingle):
    if both_arraylike(L, gsingle):
        L, gsingle = np.meshgrid(L, gsingle)

    rtgouy = rtgouy_of_gsingle(gsingle)
    return modesep_adjust(rtgouy, L)

def modesep_of_gcav(L, gcav):
    rtgouy = rtgouy_of_gcav(gcav)
    return modesep_adjust(rtgouy, L)

def modesep_of_w(L, wl, w):
    rtgouy = rtgouy_of_w(L, wl, w)
    return modesep_adjust(rtgouy, L)

def modesep_of_divang(L, wl, theta):
    rtgouy = rtgouy_of_divang(L, wl, theta)
    return modesep_adjust(rtgouy, L)

def eigenmode_of_Rc(L, Rc):
    if isinstance(L, np.ndarray) or isinstance(Rc, np.ndarray):
        print("WARNING: Computing ABCD matrices over data ranges is not yet supported, "
              "setting eigenmode to None.")
        return None

    ABCD = abcd(L, Rc, Rc)

    C = ABCD[1][0]
    D_minus_A = ABCD[1][1] - ABCD[0][0]
    minus_B = -ABCD[0][1]

    sqrt_term = cmath.sqrt(D_minus_A * D_minus_A - 4 * C * minus_B)
    upper = 0.5 * (D_minus_A + sqrt_term) / C
    lower = 0.5 * (D_minus_A - sqrt_term) / C

    if np.imag(upper) > 0.0:
        return upper
    elif np.imag(lower) > 0.0:
        return lower

FUNC_DEPENDENCIES_MAP = {
    w_of_gsingle : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.BEAMSIZE,
    ),
    w_of_gcav : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.CAV_GFACTOR),
        Parameter.BEAMSIZE,
    ),
    w_of_rtgouy : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GOUY),
        Parameter.BEAMSIZE,
    ),
    w_of_divang : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.BEAMSIZE,
    ),
    w0_of_gsingle : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.WAISTSIZE,
    ),
    w0_of_gcav : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.CAV_GFACTOR),
        Parameter.WAISTSIZE,
    ),
    w0_of_rtgouy : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GOUY),
        Parameter.WAISTSIZE,
    ),
    z0_symmetric : (
        (Parameter.CAV_LENGTH, ),
        Parameter.WAISTPOS,
    ),
    gsingle_of_roc : (
        (Parameter.CAV_LENGTH, Parameter.ROC),
        Parameter.GFACTOR_SINGLE
    ),
    gsingle_of_w : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.GFACTOR_SINGLE
    ),
    gsingle_of_rtgouy : (
        (Parameter.GOUY, ),
        Parameter.GFACTOR_SINGLE
    ),
    gsingle_of_divang : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.GFACTOR_SINGLE
    ),
    gsingle_of_gcav : (
        (Parameter.CAV_GFACTOR, ),
        Parameter.GFACTOR_SINGLE
    ),
    gcav_of_roc : (
        (Parameter.CAV_LENGTH, Parameter.ROC),
        Parameter.CAV_GFACTOR
    ),
    gcav_of_gsingle : (
        (Parameter.GFACTOR_SINGLE, ),
        Parameter.CAV_GFACTOR
    ),
    gcav_of_w : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.CAV_GFACTOR
    ),
    gcav_of_rtgouy : (
        (Parameter.GOUY, ),
        Parameter.CAV_GFACTOR
    ),
    gcav_of_divang : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.CAV_GFACTOR
    ),
    rtgouy_of_gsingle : (
        (Parameter.GFACTOR_SINGLE, ),
        Parameter.GOUY,
    ),
    rtgouy_of_gcav : (
        (Parameter.CAV_GFACTOR, ),
        Parameter.GOUY,
    ),
    rtgouy_of_w : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.GOUY,
    ),
    rtgouy_of_divang : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.GOUY,
    ),
    divang_of_gsingle : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.DIVERGENCE,
    ),
    divang_of_gcav : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.CAV_GFACTOR),
        Parameter.DIVERGENCE,
    ),
    divang_of_w : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.DIVERGENCE,
    ),
    divang_of_rtgouy : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GOUY),
        Parameter.DIVERGENCE,
    ),
    modesep_of_rtgouy : (
        (Parameter.CAV_LENGTH, Parameter.GOUY),
        Parameter.MODESEP,
    ),
    modesep_of_gsingle : (
        (Parameter.CAV_LENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.MODESEP,
    ),
    modesep_of_gcav : (
        (Parameter.CAV_LENGTH, Parameter.CAV_GFACTOR),
        Parameter.MODESEP,
    ),
    modesep_of_w : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.MODESEP,
    ),
    modesep_of_divang : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.MODESEP,
    ),
    roc_of_gsingle : (
        (Parameter.CAV_LENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.ROC,
    ),
    eigenmode_of_Rc : (
        (Parameter.CAV_LENGTH, Parameter.ROC),
        Parameter.EIGENMODE,
    ),
}
