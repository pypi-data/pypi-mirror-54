import numpy as np

from .. import CONFIG


class CavCalcError(Exception): pass


def dummy_return(value):
    return value

def both_arraylike(x, y):
    return isinstance(x, np.ndarray) and isinstance(y, np.ndarray)

def save_result(result, filename):
    """Save an array of data to either a .npy file or txt file,
    depending upon `filename`."""
    if filename is None: return
    if filename.endswith(".npy"):
        np.save(filename, result)
    else:
        np.savetxt(filename, result)

def quit_print(msg, from_command_line=True):
    if from_command_line:
        print(msg)
        exit(-1)
    else:
        raise CavCalcError(msg)

def bug(msg, from_command_line):
    if "bug_reporting" in CONFIG and CONFIG["bug_reporting"].getboolean("report"):
        # TODO send an email with contents = msg
        pass

    quit_print(msg, from_command_line)
