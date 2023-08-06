import argparse
import numpy as np

from .parameter import Parameter
from .parameter import ARG_PARAM_MAP, TARGET_PARAM_MAP
from .parameter import param_to_command_arg
from .parsing import add_parser_arguments, handle_parser_namespace
from .units import standard_units_from_param
from .utilities import CavCalcError

_SHORTARG_PARAM = {
    "w" : Parameter.BEAMSIZE,
    "w0" : Parameter.WAISTSIZE,
    "g" : Parameter.CAV_GFACTOR,
    "gouy" : Parameter.GOUY,
    "div" : Parameter.DIVERGENCE,
    "FSR" : Parameter.FSR,
    "fsr" : Parameter.FSR,
    "FWHM" : Parameter.FWHM,
    "fwhm" : Parameter.FWHM,
    "finesse" : Parameter.FINESSE,
    "pole" : Parameter.POLE,
    "modesep" : Parameter.MODESEP,
    "w1" : Parameter.BEAMSIZE_ITM,
    "w2" : Parameter.BEAMSIZE_ETM,
    "g1" : Parameter.GFACTOR_ITM,
    "g2" : Parameter.GFACTOR_ETM,
    "gs" : Parameter.GFACTOR_SINGLE,
    "L" : Parameter.CAV_LENGTH,
    "R1" : Parameter.REFLECTIVITY_ITM,
    "R2" : Parameter.REFLECTIVITY_ETM,
    "wl" : Parameter.WAVELENGTH,
    "Rc" : Parameter.ROC,
    "Rc1" : Parameter.ROC_ITM,
    "Rc2" : Parameter.ROC_ETM
}

def calculate(target="all", **kwargs):
    """Calculates any target parameter (defaulting to all computable parameters) from an
    arbitrary number of physical arguments.

    Parameters
    ----------
    target : str or :class:`.Parameter`, optional
        The target parameter to compute, can be specified as a string (see note above) or
        a constant of the enum :class:`.Parameter`. Defaults to `"all"` so that the function
        computes all the parameters it can from the given inputs.

    **kwargs
        See the note above for details.

    Returns
    -------
    out : :class:`.Output`
        The output object containing the results and methods for plotting them.
    """
    if (target is None or
            (target not in TARGET_PARAM_MAP.keys() and
             target not in TARGET_PARAM_MAP.values())
       ):
       raise CavCalcError(f"Unrecognised target: {target} in call to calculate.")

    command = [target]
    for arg, value in kwargs.items():
        if (arg not in ARG_PARAM_MAP.keys() and arg not in ARG_PARAM_MAP.values()
            and arg not in _SHORTARG_PARAM.keys()):
            raise CavCalcError(f"Unrecognised argument: {arg} in arguments to calculate.")

        if arg in ARG_PARAM_MAP.keys():
            parg = ARG_PARAM_MAP[arg]
        elif arg in _SHORTARG_PARAM.keys():
            parg = _SHORTARG_PARAM[arg]
        else:
            parg = arg

        if not isinstance(value, tuple):
            v_in_spec_units, units_str = value, standard_units_from_param(parg)
        else:
            if len(value) != 2:
                raise CavCalcError(f"Expected tuple of size 2 for argument: {arg} but got size: {len(value)}.")
            v_in_spec_units, units_str = value

        # form the command
        if isinstance(v_in_spec_units, np.ndarray):
            start = np.min(v_in_spec_units)
            stop = np.max(v_in_spec_units)
            num = v_in_spec_units.size

            if num == 2:
                raise CavCalcError("Data ranges of size 2 are currently not supported due "
                                   "to the conflict with upper/lower quadrant computations. "
                                   "This is a non-trivial issue and so will be fixed at a later date.")

            command.append(f"{param_to_command_arg(parg)}")
            command.append(f"{start} {stop} {num} {units_str}")
        else:
            command.append(f"{param_to_command_arg(parg)}")
            command.append(f"{v_in_spec_units}{units_str}")

    parser = argparse.ArgumentParser()
    # add all the available arguments
    add_parser_arguments(parser)
    # parse the args provided into a Namespace
    args = parser.parse_args(command)
    return handle_parser_namespace(args, from_command_line=False)
