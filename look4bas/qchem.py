#!/usr/bin/env python3
from . import elements
from .constants import NUMBER_TO_AM
from warnings import warn


def dumps(data, elem_list=elements.iupac_list()):
    """
    Take a list of dicts containing the entries
        atnum:     atomic number
        functions: list of dict with the keys:
            angular_momentum  Angular momentum of the function
            coefficients      List of contraction coefficients
            exponents         List of contraction exponents
    and dump a string representing this basis set definition
    in Gaussian94 format.

    Note, that as of now potential ECP data present in the basis
    is ignored.
    """
    warn("Dumping basis sets in Q-Chem format is experimental.")

    first = True
    lines = []
    lines.append("$basis")
    for atom in data:
        if first:
            first = False
        else:
            lines.append("****")

        lines.append(elem_list[atom["atnum"]]["symbol"] + "     0")
        for fun in atom["functions"]:
            lfun = len(fun["coefficients"])
            if lfun != len(fun["exponents"]):
                raise ValueError("Length of coefficients and length of exponents "
                                 "in contraction specification need to agree.")

            am = NUMBER_TO_AM[fun["angular_momentum"]]
            lines.append("{}   {}   1.00".format(am, lfun))

            for i, coeff in enumerate(fun["coefficients"]):
                exp = fun["exponents"][i]
                lines.append("{0:15.7f}             {1: #11.8G}".format(exp, coeff))
    lines.append("$end")

    for atom in data:
        if "ecp" in atom:
            warn(dumps.__name__ + " currently ignores any ECP "
                 "definitions parsed.")
            break

    return "\n".join(lines)
