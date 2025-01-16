# This function reads the output XML file, extracts the XYZ coordinates, 
# and writes them into an XYZ file. The latter can be read or visualized elsewhere, e.g. in VESTA

import xml.etree.ElementTree as ET
import numpy as np

import sys

def parse_xml_to_xyz(xml_file, xyz_file):
    # Parse the XML file
    # create element tree object 
    tree = ET.parse(xml_file)
    # get root element 
    root = tree.getroot()

    # Open the XYZ file for writing
    with open(xyz_file, 'w') as f:
        # Find all atomic species and coordinates ==============================================
        atoms = root.findall('.//output/atomic_structure/atomic_positions/atom'); # print(atoms)
        num_atoms = len(atoms); # print(num_atoms)
          
        # Write the number of atoms at the top of the XYZ file
        f.write(f"{num_atoms}\n")
        f.write(f"Generated from QuantumEspresso: {xml_file}\n")

        # Extract species and coordinates
        print("Extracted XYZ coordinates:")
        for atom in atoms:
            # Get attribute "name" in the entry
            species = atom.get('name');
            coords = atom.text;    # Access data between <></>    
            
            # Convertion to float 
            coords_float = [float(coord_comp) for coord_comp in coords.split()]; # IS THERE A SOLUTION WITHOUT FOR-LOOP?
            coords_float = np.array(coords_float)   # Convert to Numpy array type   # https://www.geeksforgeeks.org/convert-python-list-to-numpy-arrays/

            # Convert the vector from fractional into Cartesian coords using the unite cell's parameters
            coords_XYZ = coords_float*Hartree_au_to_Angstrom
            delimeter = "   "; 
            coords_XYZ_str = delimeter.join(map(str, coords_XYZ))   # Convert to string without square brackets # https://stackoverflow.com/questions/34201288/write-a-txt-from-list-without-brackets
            output_line = f"{species}   {coords_XYZ_str}"
            print(output_line)
            f.write(output_line + "\n")
            
        # Total energy =====================================================================
        total_energy_Hr = root.find('.//total_energy/etot').text
        total_energy_Hr = float(total_energy_Hr)        
        Hartree_to_Ry = 2.0
        total_energy_Ry = total_energy_Hr*Hartree_to_Ry
        Ry_to_eV = 13.6057  # eV
        total_energy_eV = total_energy_Ry*Ry_to_eV
        print()
        print("Total energy =")
        print(f"{total_energy_Hr} [Hartree]")
        print(f"{total_energy_Ry} [Ry] ????????")
        print(f"{total_energy_eV} [eV] ????????")


# Conversion coefficient
Hartree_au_to_Angstrom = 0.5291772105

# Read filenames
output_xml_file = sys.argv[1]   # './pwscf.save/data-file-schema.xml'  # Input XML file
output_xyz_file = sys.argv[2]   # 'data-file-schema.xyz'  # Output XYZ filename

# Call function
parse_xml_to_xyz(output_xml_file, output_xyz_file)
print(f"\nSuccessfully created XYZ file: \n{output_xyz_file}\n")
