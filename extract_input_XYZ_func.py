# This function reads the output XML file, extracts the XYZ coordinates of the last iteration of the QE optimisation routine, 
# and writes the coordinates into an XYZ file. The latter can be read or visualized elsewhere, e.g. in VESTA

import re

import sys


def parse_qe_input(filename):
    """
    Parses the Quantum ESPRESSO input file to extract lattice parameters, atomic species, and XYZ coordinates.

    Parameters:
    filename (str): Path to the Quantum ESPRESSO input file.

    Returns:
    tuple: A tuple containing a list of lattice parameters and a list of atomic positions.
           - lattice_params (list): Contains lattice vectors as lists of floats.
           - atoms (list): Contains tuples of (species, x, y, z).
    """
    lattice_params = []
    #atoms = []
    in_cell_parameters = False
    in_atomic_positions = False
    
    with open(filename, 'r') as file:
        for line in file: # Read line by line
            # Detect the start of CELL_PARAMETERS block
            if 'CELL_PARAMETERS' in line:
                in_cell_parameters = True
                in_atomic_positions = False
                continue

            # Detect the start of ATOMIC_POSITIONS block
            if 'ATOMIC_POSITIONS' in line:
                atoms = []
                in_cell_parameters = False
                in_atomic_positions = True
                continue

            # Process lattice parameters
            if in_cell_parameters:
                if re.match(r'^\s*[-+]?\d*\.\d+|\d+', line):
                    # print(line)
                    lattice_vector = list(map(float, line.split()))
                    #print(lattice_vector)
                    lattice_params.append(lattice_vector)

            # Process atomic positions
            if in_atomic_positions:
                if re.match(r'^\s*\w+\s+[-+]?\d*\.\d+|\d+', line):
                    #print(line)
                    parts = line.split()
                    species = parts[0]
                    x, y, z = map(float, parts[1:4])
                    atoms.append((species, x, y, z))
    
    return lattice_params, atoms



def write_xyz(filename, atoms, lattice_params):
    """
    Writes the atomic positions and lattice parameters to an XYZ file.

    Parameters:
    filename (str): Path to the output XYZ file.
    atoms (list): List of tuples containing atomic species and coordinates.
    lattice_params (list): List of lattice vectors.
    """
    with open(filename, 'w') as file:
        # Write the number of atoms and a comment line with lattice parameters
        file.write(f"{len(atoms)}\n")
        lattice_str = "Lattice=\""
        for vec in lattice_params:
            lattice_str += " ".join(map(str, vec)) + " "
        lattice_str = lattice_str.strip() + "\"\n"
        file.write(lattice_str)

        #print(atoms)

        # Write atomic species and coordinates
        for atom in atoms:
            species, x, y, z = atom
            file.write(f"{species} {x:.6f} {y:.6f} {z:.6f}\n")
            #print(f"{species} {x:.6f} {y:.6f} {z:.6f}\n")



# Read filenames
qe_input_file =   sys.argv[1]   # 'output_S8_1116225.out'  # Input XML file
xyz_output_file = sys.argv[2]   # 'data-file-schema.xyz'  # Output XYZ filename

# Parse Quantum ESPRESSO input and write to XYZ
lattice_params, atoms = parse_qe_input(qe_input_file)   # Call function
write_xyz(xyz_output_file, atoms, lattice_params)

print(f"\nSuccessfully created XYZ file: \n{xyz_output_file}\n")
