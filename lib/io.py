from typing import List, TypedDict
from re import split, compile, match
import matplotlib.pyplot as plt
import pandas as pd
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
            obj['reac'] = removeR_(obj['reac'])
            constraints['obj'].append(obj)
        elif L.count('\t') == 2:
            flux = split(r'\t+', L)
            flux = {
                'reac': str(flux[0]), 
                'minbound': float(flux[1]), 
                'maxbound': float(flux[2])
            }
            flux['reac'] = removeR_(flux['reac'])
            constraints['flux'].append(flux)
        elif '=' in L:
            constraints['equations'].append(analyzeEquation(L))
        else:
            raise Exception(f'{bcolors.FAIL}Error:{bcolors.ENDC} ill-formed constraints file.')
    return constraints


def analyzeEquation(equation_string: str) -> dict:
    equation: dict = {
        'sign': str,
        'left_coeffs': [],
        'right_coeffs': [],
        'left_reacs': [],
        'right_reacs': []
    }
    signs = {'<', '<=', '=', '=>', '>'}
    
    equation_words = equation_string.split()
    
    # Get equation sign and check that there is only one sign.
    equation_sign = [
        (idx, word) for idx, word in enumerate(equation_words) if word in signs
    ]
    if len(equation_sign) == 1:
        equation['sign'] = equation_sign[0][1]
        sign_position = equation_sign[0][0]
    elif len(equation_sign) == 0: raise Exception(
            f"There is no sign in this equation: {equation_string}"
        )
    else: raise Exception(
            f"There are too many signs in this equation: {equation_string}"
        )

    # Add reactions and coefficients to their side of the equation
    next_coeff_sign = None
    for idx, word in enumerate(equation_words):
        # Check side of equation
        if idx == sign_position:
            next_coeff_sign = None
            continue
        elif idx < sign_position:
            coeff_key, reac_key = 'left_coeffs', 'left_reacs'
        else:
            coeff_key, reac_key = 'right_coeffs', 'right_reacs'
        
        if word in ('-', '+'):
            if next_coeff_sign == None:
                next_coeff_sign = word
                continue
            else:
                raise Exception("Two + or - signs in a row.")
        elif word.count('*') == 1:
            coeff, reac = word.split('*')
        elif bool(match(r'^[\+\-][a-zA-Z0-9_]+$', word)):
            coeff, reac = word[0], word[1:]
        elif word.count('_'):
            coeff, reac = 1, word
        else:
            raise Exception(
                f'"{word}" in [{equation_string}] could '
                + 'not be parsed'
            )    
        try:
            coeff = float(coeff)
        except ValueError:
            raise ValueError(
                f'The coefficient for "{reac}" in [{equation_string}] '
                + 'is not a number.'
            )
        reac = removeR_(reac)
        if next_coeff_sign == '-':
            equation[coeff_key].append(-coeff)
            equation[reac_key].append(reac)
            next_coeff_sign = None
        else:
            equation[coeff_key].append(coeff)
            equation[reac_key].append(reac)
            next_coeff_sign = None
    # Check that reactions/coefficients numbers are coherent.
    return(equation)
            
def removeR_(reac_name: str) -> str:
    return reac_name[2:] if reac_name.startswith('R_') else reac_name

def loadConfig(config_file) -> dict:
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    config['biomass_reac'] = {organ: removeR_(reac_name)
                                   for organ, reac_name
                                   in config['biomass_reac'].items()}
    config['sucrose_ex_reac'] = removeR_(config['sucrose_ex_reac'])
    return config

def editCobraConfig(default_cobra_config, config):
    bounds = config['cobra_config']['bounds']
    solver = config['cobra_config']['solver']
    if bounds != '': default_cobra_config.bounds = bounds
    if solver != '': default_cobra_config.solver = solver
    return default_cobra_config
    
def drawTimeSeries(time_series: dict, title: str, out_path: str) -> None:
    n_loops = len(list(time_series.values())[0])
    for key in time_series:
        plt.plot(range(1, n_loops+1), time_series[key], label = key)
    plt.title(title)
    plt.legend()
    plt.savefig(out_path)

def writeFbaFluxTable(flux_df: pd.DataFrame, out_path: str) -> None:
    flux_df.to_csv(out_path, sep='\t', index=True)
