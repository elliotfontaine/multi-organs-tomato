import subprocess
import cobra
from lib.io import getObjectiveFromResults

def runFba(flexflux: str, sbml: str, constraints: str, out: str):
    subprocess.run(
        [
            'bash',
            f'/mnt/c/{flexflux}/Flexflux.sh',
            f'FBA -s /mnt/c/{sbml} -cons /mnt/c/{constraints} -out {out}'
        ]
    )

def computeInitialLeafBiomass(flexflux, sbml, leaf_constraints, results_dir) -> float:
    leaf_result_file = f'{results_dir}/FBA_leaf_1.txt'
    runFba(flexflux, sbml, leaf_constraints, leaf_result_file)
    return getObjectiveFromResults(leaf_result_file)  

def computeLeafBiomass(sbml, leaf_constraints, Y_root, Y_stem) -> float:
    return

def computeRootSucrose(sbml, root_constraints, X_leaf, Z_leaf, Z_stem) -> float:
    return

def computeStemSucrose(sbml, stem_constraints, X_leaf) -> float:
    return