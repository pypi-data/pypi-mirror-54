import numpy as np
from amlearn.utils.data import read_lammps_dump
from amlearn.featurize.symmetry_function import \
    BPRadialFunction, BPAngularFunction

"""
This is an example script of deriving B-P symmetry functinos for each atom, 
based on the Fortran source codes in amlearn/featurize/featurizers/src/
bp_symmfunc.f90. Please make sure to compile the Fortran code using
f2py before running this script. 
"""

system = ["Cu65Zr35", "qr_5plus10^10"]

lammps_file = "xxx/dump.lmp"
structure, bds = read_lammps_dump(lammps_file)

output_path = "xxx/xxx"

# Calculating B-P radial symmetry function
ref_atom_number = "29" # Cu
atom_type_symbols = np.array([1, 2])
delta_r=0.1
n_r=50

bp_radial_function = \
    BPRadialFunction(ref_atom_number, atom_type_symbols, bds,
                     delta_r=delta_r, n_r=n_r, output_path=output_path)

radial_funcs_df = bp_radial_function.fit_transform(structure)

# Calculating B-P angular symmetry function
ksaais = np.array([14.633, 14.633, 14.638, 14.638, 2.554, 2.554, 2.554, 2.554,
                   1.648, 1.648, 1.204, 1.204, 1.204, 1.204, 0.933, 0.933,
                   0.933, 0.933, 0.695, 0.695, 0.695, 0.695])
lambdas = np.array([-1, 1, -1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1, 1, 1, 1, 1])
zetas = np.array([1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2,
                  4, 16, 1, 2, 4, 16, 1, 2, 4, 16])

bp_angular_function = \
    BPAngularFunction(ref_atom_number, atom_type_symbols,
                      ksaais, lambdas, zetas, bds, output_path=output_path)

angular_funcs_df = bp_angular_function.fit_transform(structure)
