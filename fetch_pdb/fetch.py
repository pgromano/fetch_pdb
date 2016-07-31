import numpy as np
import mdtraj as md
import warnings
from six.moves.urllib import request

def fetch(ID):
    try:
        # Fetch from RCSB
        print("Fetching structure from RCSB")
        url = 'http://www.rcsb.org/pdb/files/%s.pdb' % ID
        request.urlretrieve(url, ID + ".pdb")
    except:
        warnings.warn(str(ID)+" not found in RCSB:PDB.")
        pass

    molecule = md.load(ID+".pdb").remove_solvent()
    molecule = check_hydrogens(molecule, ID)

    if molecule.xyz.shape[0] == 1:
        warnings.warn("""PDB file contains only one conformation. For accurate results, it is recommended to supply conformation data from NMR or CryoEM structures. Proceed with caution.
        """)
    return molecule

def check_hydrogens(molecule, ID):
    # Check that Hydrogens are in structure
    if len(molecule.top.select("name == H")) == 0:
        # If absent, then add Hydrogens using the Amber99sb force-field
        try:
            from simtk.openmm.app import PDBFile, Modeller, ForceField
            pdb = PDBFile(ID + ".pdb")
            modeller = Modeller(pdb.topology, pdb.positions)
            forcefield = ForceField('amber99sb.xml','tip3p.xml')
            modeller.addHydrogens(forcefield)
            PDBFile.writeFile(modeller.topology, modeller.positions, open(ID + ".pdb", 'w'))
            molecule = md.load(ID + ".pdb").remove_solvent()
        except:
            warnings.warn("""PDB topology missing Hydrogens. Either manually add
            or install OpenMM through SIMTK to automatically correct.""")
            pass
    return molecule
