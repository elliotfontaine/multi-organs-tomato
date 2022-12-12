import subprocess
from typing import List, TypedDict
import yaml
import os
os.system("color")


path_flexflux = "Users/ElliotFontaine/Documents/FlexFlux2.2"
path_sbml = "Users/ElliotFontaine/Documents/MultiOrganes/tomato.xml"
path_constraints = "Users/ElliotFontaine/Documents/MultiOrganes/constraints_tomato_day.txt"
path_fba_results = "Users/ElliotFontaine/Documents/MultiOrganes/fba_results"

# subprocess.run(
#     [
#         'bash',
#         f'/mnt/c/{path_flexflux}/Flexflux.sh',
#         f'FBA -s /mnt/c/{path_sbml} -cons /mnt/c/{path_constraints} -out FBA_results.txt'
#     ]
# )

class Constraints(TypedDict):
    obj: List[str]
    flux: List[str]
    equations: List[str]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(flexflux, sbml, cons_leaf, cons_stem, cons_root, ):
    X_leaf: float = 0
    X_root: float = 0
    X_stem: float = 0
    Y_root: float = 0
    Y_stem: float = 0
    Z_leaf: float = 0
    Z_stem: float = 0

    computeInitialLeafBiomass()
    
    
def runFba(flexflux: str, sbml: str, constraints: str, out: str):
    subprocess.run(
        [
            'bash',
            f'/mnt/c/{flexflux}/Flexflux.sh',
            f'FBA -s /mnt/c/{sbml} -cons /mnt/c/{constraints} -out {out}'
        ]
    )

def getObjectiveFromResults(fba_results_file) -> float:
    f = open(fba_results_file, 'r')
    next(f)
    next(f)
    objective: str = f.readline()[6:]
    f.close()
    return float(objective)

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

def parseConstraintsFile(constraints_file) -> Constraints:
    # check file presence
    f = open(constraints_file, 'r')
    lines_list = f.read().splitlines()
    f.close()
    constraints: Constraints = {'obj': [], 'flux': [], 'equations': []}
    for l in lines_list:
        print(l)
        if l.startswith('#') or l == '' or l == 'EQUATIONS':
            continue
        elif l.startswith('obj : '):
            constraints['obj'].append(l)
        elif '\t' in l:
            constraints['flux'].append(l)
        elif '=' in l:
            constraints['equations'].append(l)
        else:
            raise SystemExit(f'{bcolors.FAIL}Error:{bcolors.ENDC} ill-formed constraints file.')    
    return constraints

def drawTimeSeries(series_X_leaf, others):
    return


print(getObjectiveFromResults('FBA_results.txt'))
print(parseConstraintsFile('constraints_tomato_day.txt'))