from typing import List, TypedDict
from re import split, compile
import yaml
import os
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
    equations: List[dict]

def parseConstraintsFile(constraints_file) -> Constraints:
    pass # TO IMPLEMENT: check file presence
    f = open(constraints_file, 'r')
    lines_list = f.read().splitlines()
    f.close()
    constraints: Constraints = {'obj': [], 'flux': [], 'equations': []}
    for L in lines_list:
        if L.startswith('#') or L in ('', 'EQUATIONS'):
            continue
        elif (compile('obj : MAX\(.*\)').match(L) or
              compile('obj : MIN\(.*\)').match(L)):
            obj = {'reac': L[10:-1], 'coeff': 1, 'direction': L[6:9].lower()}
            if obj['reac'].startswith('-'):
                obj['reac'] = obj['reac'][1:]
                obj['coeff'] = -1
            if obj['reac'].startswith('R_'): obj['reac'] = obj['reac'][2:]
            constraints['obj'].append(obj)
        elif L.count('\t') == 2:
            flux = split(r'\t+', L)
            flux = {
                'reac': str(flux[0]), 
                'minbound': float(flux[1]), 
                'maxbound': float(flux[2])
            }
            if flux['reac'].startswith('R_'): flux['reac'] = flux['reac'][2:]
            constraints['flux'].append(flux)
        elif '=' in L:
            constraints['equations'].append(L) # append(analyzeEquation(L))
        else:
            raise SystemExit(f'{bcolors.FAIL}Error:{bcolors.ENDC} ill-formed constraints file.')
    return constraints

# def analyzeEquation(equation_string: str) -> dict:
#     equation: dict = {
#         'sign': str,
#         'left_metabs': [],
#         'right_metabs': [],
#         'left_coeffs': [],
#         'right_coeffs': []
#     }
#     string_elements = equation_string.split()
#     after_sign = False
#     for element in string_elements:
#         if element in ('<', '=', '>'):
#             equation['sign'] = element
#             after_sign = True
#         if element.count('*'):
# UNFINISHED
            
        

def loadConfig(config_file) -> dict:
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def editCobraConfig(default_cobra_config, config):
    bounds = config['cobra_config']['bounds']
    solver = config['cobra_config']['solver']
    if bounds != '': default_cobra_config.bounds = bounds
    if solver != '': default_cobra_config.solver = solver
    return default_cobra_config
    
def drawTimeSeries(series_X_leaf, others):
    pass
