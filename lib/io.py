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
    obj: List[dict]
    flux: List[dict]
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
        elif compile('obj : MAX\(.*\)').match(L) or compile('obj : MIN\(.*\)').match(L):
            obj = {'reac': L[10:-1], 'direction': L[6:9].lower()}
            obj['reac'] = obj['reac'][2:] if obj['reac'].startswith('R_') else obj['reac']
            constraints['obj'].append(obj)
        elif L.count('\t') == 2:
            flux = split(r'\t+', L)
            flux = {
                'reac': str(flux[0]), 
                'minbound': float(flux[1]), 
                'maxbound': float(flux[2])
            }
            flux['reac'] = flux['reac'][2:] if flux['reac'].startswith('R_') else flux['reac']
            constraints['flux'].append(flux)
        elif '=' in L:
            constraints['equations'].append(L)
        else:
            raise SystemExit(f'{bcolors.FAIL}Error:{bcolors.ENDC} ill-formed constraints file.')
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
    pass