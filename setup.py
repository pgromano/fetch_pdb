from setuptools import setup

setup(name = 'fetch_pdb',
    version = '0.1',
    description = 'Python API for fetching PDB files from RCSB:Protein Data Bank',
    #url = 'https://github.com/pgromano/fetch_pdb',
    packages = ['fetch_pdb'],
    install_requires=[
        'mdtraj',
        'numpy'
    ],
    zip_safe = False
)
