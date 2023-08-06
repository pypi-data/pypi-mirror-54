import numpy as np

from . import constants
from .parameter import Parameter
from .utilities import both_arraylike

### Generic cavity properties

def fsr(L):
    return 0.5 * constants.SPEED_OF_LIGHT / L

def finesse(R1, R2):
    if both_arraylike(R1, R2):
        R1, R2 = np.meshgrid(R1, R2)
    return 0.5 * np.pi / np.arcsin(0.5 * (1 - np.sqrt(R1*R2)) / np.power(R1*R2, 0.25))

def fwhm(L, R1, R2):
    if both_arraylike(L, R1):
        L, R1 = np.meshgrid(L, R1)
    elif both_arraylike(L, R2):
        L, R2 = np.meshgrid(L, R2)
    return fsr(L)/finesse(R1, R2)

def pole(L, R1, R2):
    return 0.5 * fwhm(L, R1, R2)


FUNC_DEPENDENCIES_MAP = {
    fsr  : (
        (Parameter.CAV_LENGTH, ),
        Parameter.FSR,
    ),
    finesse : (
        (Parameter.REFLECTIVITY_ITM, Parameter.REFLECTIVITY_ETM),
        Parameter.FINESSE,
    ),
    fwhm : (
        (Parameter.CAV_LENGTH, Parameter.REFLECTIVITY_ITM, Parameter.REFLECTIVITY_ETM),
        Parameter.FWHM,
    ),
    pole : (
        (Parameter.CAV_LENGTH, Parameter.REFLECTIVITY_ITM, Parameter.REFLECTIVITY_ETM),
        Parameter.POLE,
    ),
}
