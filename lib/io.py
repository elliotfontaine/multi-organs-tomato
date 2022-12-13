from typing import List, TypedDict
import yaml
import os
from re import split, compile
os.system("color")

class bcolors:
    '''used for console outputs (errors, warnings)'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Constraints(TypedDict):
    obj: List[tuple]
    flux: List[tuple]
    equations: List[str]

def parseConstraintsFile(constraints_file) -> Constraints:
    pass # TO IMPLEMENT: check file presence
    f = open(constraints_file, 'r')
    lines_list = f.read().splitlines()
    f.close()
    constraints: Constraints = {'obj': [], 'flux': [], 'equations': []}
    for L in lines_list:
        if L.startswith('#') or L == '' or L == 'EQUATIONS':
            continue
        elif compile('obj : MAX\(.*\)').match(L):
            constraints['obj'].append((L[10:-1], 'maximize'))
        elif compile('obj : MIN\(.*\)').match(L):
            constraints['obj'].append((L[10:-1], 'minimize'))
        elif L.count('\t') == 2:
            flux = split(r'\t+',L)
            flux = (str(flux[0]), float(flux[1]), float(flux[2])) # force types
            constraints['flux'].append(flux)
        elif '=' in L:
            constraints['equations'].append(L)
        else:
            raise SystemExit(f'{bcolors.FAIL}Error:{bcolors.ENDC} ill-formed constraints file.')
    constraints['obj'] = [(obj[0][2:], obj[1]) if obj[0].startswith('R_') else obj for obj in constraints['obj']]
    constraints['flux'] = [(flux[0][2:], flux[1], flux[2]) if flux[0].startswith('R_') else flux for flux in constraints['flux']]
    return constraints

def loadConfig(config_file):
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def getObjectiveFromResults(fba_results_file) -> float:
    f = open(fba_results_file, 'r')
    next(f)
    next(f)
    objective: str = f.readline()[6:]
    f.close()
    return float(objective)

def drawTimeSeries(series_X_leaf, others):
    return