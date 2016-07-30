import numpy as np
import mdtraj as md
import warnings
from urllib.request import urlretrieve

def fetch(ID):
        try:
            # Fetch from RCSB
            print("Fetching structure from RCSB")
            url = 'http://www.rcsb.org/pdb/files/%s.pdb' % ID
            urlretrieve(url, ID + ".pdb")
        except:
            warnings.warn(str(ID)+" not found in RCSB:PDB.")
            pass

    molecule = solvent(md.load(ID + ".pdb"))
    molecule = hydrogens(molecule)

    if molecule.xyz.shape[0] == 1:
        warnings.warn("""PDB file contains only one conformation. For accurate results, it is recommended to supply conformation data from NMR or CryoEM structures. Proceed with caution.
        """)
    return molecule

def solvent(molecule):
    return molecule.remove_solvent()

def hydrogens(molecule):
    # Check that Hydrogens are in structure
    if len(molecule.top.select("name == H")) == 0:
        # If absent, then add Hydrogens using the Amber99sb force-field
        warnings.warn("""Hydrogen atoms are not located within the topology file. Protein structure will be corected using Amber99sb.xml force-field""")
        from simtk.openmm.app import PDBFile, Modeller, ForceField
        pdb = PDBFile(fetch + ".pdb")
        modeller = Modeller(pdb.topology, pdb.positions)
        forcefield = ForceField('amber99sb.xml','tip3p.xml')
        modeller.addHydrogens(forcefield)
        PDBFile.writeFile(modeller.topology, modeller.positions, open(fetch + ".pdb", 'w'))
        molecule = md.load(fetch + ".pdb").remove_solvent()
    return molecule
