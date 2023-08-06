import cmath
import numpy as np

from .parameter import Parameter
from .utilities import both_arraylike, modesep_adjust
from .utilities.maths import abcd


### Beam radius relations

def w1_of_g1g2(L, wl, g1, g2):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, g1):
        L, g1 = np.meshgrid(L, g1)
    elif both_arraylike(L, g2):
        L, g2 = np.meshgrid(L, g2)
    elif both_arraylike(wl, g1):
        wl, g1 = np.meshgrid(wl, g1)
    elif both_arraylike(wl, g2):
        wl, g2 = np.meshgrid(wl, g2)
    elif both_arraylike(g1, g2):
        g1, g2 = np.meshgrid(g1, g2)
    return np.sqrt(L * wl / np.pi * np.sqrt(g2 / (g1 * (1 - g1 * g2))))

def w2_of_g1g2(L, wl, g1, g2):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, g1):
        L, g1 = np.meshgrid(L, g1)
    elif both_arraylike(L, g2):
        L, g2 = np.meshgrid(L, g2)
    elif both_arraylike(wl, g1):
        wl, g1 = np.meshgrid(wl, g1)
    elif both_arraylike(wl, g2):
        wl, g2 = np.meshgrid(wl, g2)
    elif both_arraylike(g1, g2):
        g1, g2 = np.meshgrid(g1, g2)
    return np.sqrt(L * wl / np.pi * np.sqrt(g1 / (g2 * (1 - g1 * g2))))

def w0_of_g1g2(L, wl, g1, g2):
    if both_arraylike(L, wl):
        L, wl = np.meshgrid(L, wl)
    elif both_arraylike(L, g1):
        L, g1 = np.meshgrid(L, g1)
    elif both_arraylike(L, g2):
        L, g2 = np.meshgrid(L, g2)
    elif both_arraylike(wl, g1):
        wl, g1 = np.meshgrid(wl, g1)
    elif both_arraylike(wl, g2):
        wl, g2 = np.meshgrid(wl, g2)
    elif both_arraylike(g1, g2):
        g1, g2 = np.meshgrid(g1, g2)
    return np.sqrt(L * wl / np.pi * np.sqrt(g1 * g2 * (1 - g1 * g2) / (g1 + g2 - 2 * g1 * g2)**2))

def z0_of_g1g2(L, g1, g2):
    if both_arraylike(L, g1):
        L, g1 = np.meshgrid(L, g1)
    elif both_arraylike(L, g2):
        L, g2 = np.meshgrid(L, g2)
    elif both_arraylike(g1, g2):
        g1, g2 = np.meshgrid(g1, g2)

    return L * g2 * (1 - g1) / (g1 + g2 - 2 * g1 * g2)

def rtgouy_of_g1g2(g1, g2):
    if both_arraylike(g1, g2):
        g1, g2 = np.meshgrid(g1, g2)

    root_g1g2 = np.sqrt(g1 * g2)
    if np.all(g1 > 0) and np.all(g2 > 0): # upper quadrant
        return 2 * np.arccos(root_g1g2)
    return 2 * np.arccos(-root_g1g2)

def __g_of_Rc(L, Rc): # NOTE don't add this to FUNC_DEPENDENCIES_MAP
    if both_arraylike(L, Rc):
        L, Rc = np.meshgrid(L, Rc)
    return 1 - L/Rc

def g1_of_Rc1(L, Rc1):
    return __g_of_Rc(L, Rc1)

def g2_of_Rc2(L, Rc2):
    return __g_of_Rc(L, Rc2)

def g_of_Rc(L, Rc1, Rc2):
    return __g_of_Rc(L, Rc1) * __g_of_Rc(L, Rc2)

def g_of_g1g2(g1, g2):
    return g1 * g2

def __Rc_of_g(L, gsingle): # NOTE don't add this to FUNC_DEPENDENCIES_MAP
    if both_arraylike(L, gsingle):
        L, gsingle = np.meshgrid(L, gsingle)
    return L / (1 - gsingle)

def Rc1_of_g1(L, g1):
    return __Rc_of_g(L, g1)

def Rc2_of_g2(L, g2):
    return __Rc_of_g(L, g2)

def modesep_of_g1g2(L, g1, g2):
    if both_arraylike(L, g1):
        L, g1 = np.meshgrid(L, g1)
    elif both_arraylike(L, g2):
        L, g2 = np.meshgrid(L, g2)

    rtgouy = rtgouy_of_g1g2(g1, g2)
    return modesep_adjust(rtgouy, L)

def eigenmode_of_Rc1Rc2(L, Rc1, Rc2):
    if isinstance(L, np.ndarray) or isinstance(Rc1, np.ndarray) or isinstance(Rc2, np.ndarray):
        print("WARNING: Computing ABCD matrices over data ranges is not yet supported, "
              "setting eigenmode to None.")
        return None

    ABCD = abcd(L, Rc1, Rc2)

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
    w1_of_g1g2 : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_ITM, Parameter.GFACTOR_ETM),
        Parameter.BEAMSIZE_ITM,
    ),
    w2_of_g1g2 : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_ITM, Parameter.GFACTOR_ETM),
        Parameter.BEAMSIZE_ETM,
    ),
    w0_of_g1g2 : (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_ITM, Parameter.GFACTOR_ETM),
        Parameter.WAISTSIZE,
    ),
    z0_of_g1g2 : (
        (Parameter.CAV_LENGTH, Parameter.GFACTOR_ITM, Parameter.GFACTOR_ETM),
        Parameter.WAISTPOS,
    ),
    rtgouy_of_g1g2 : (
        (Parameter.GFACTOR_ITM, Parameter.GFACTOR_ETM),
        Parameter.GOUY,
    ),
    g1_of_Rc1 : (
        (Parameter.CAV_LENGTH, Parameter.ROC_ITM),
        Parameter.GFACTOR_ITM,
    ),
    g2_of_Rc2 : (
        (Parameter.CAV_LENGTH, Parameter.ROC_ETM),
        Parameter.GFACTOR_ETM,
    ),
    g_of_Rc : (
        (Parameter.CAV_LENGTH, Parameter.ROC_ITM, Parameter.ROC_ETM),
        Parameter.CAV_GFACTOR,
    ),
    g_of_g1g2 : (
        (Parameter.GFACTOR_ITM, Parameter.GFACTOR_ETM),
        Parameter.CAV_GFACTOR,
    ),
    Rc1_of_g1 : (
        (Parameter.CAV_LENGTH, Parameter.GFACTOR_ITM),
        Parameter.ROC_ITM,
    ),
    Rc2_of_g2 : (
        (Parameter.CAV_LENGTH, Parameter.GFACTOR_ETM),
        Parameter.ROC_ETM,
    ),
    modesep_of_g1g2 : (
        (Parameter.CAV_LENGTH, Parameter.GFACTOR_ITM, Parameter.GFACTOR_ETM),
        Parameter.MODESEP
    ),
    eigenmode_of_Rc1Rc2 : (
        (Parameter.CAV_LENGTH, Parameter.ROC_ITM, Parameter.ROC_ETM),
        Parameter.EIGENMODE,
    ),
}
