import cobra
from cobra.io import read_sbml_model
from lib.io import *
from lib.fba import *

config = loadConfig('input/config.yaml')

constraints = parseConstraintsFile(config['paths']['leaf_cons'])
print(constraints)
main_model = read_sbml_model(config['paths']['sbml'])
# print(main_model.reactions.get_by_id('CES8_c'))

leaf_model = main_model.copy()
leaf_model.objective = 'BIOMASS_LEAF_SLY_b'
# print(leaf_model.objective.expression)
# print(leaf_model.objective.direction)

for reac in constraints['flux']:
    leaf_model.reactions.get_by_id(reac[0]).bounds = (reac[1], reac[2])



def main(flexflux, sbml, cons_leaf, cons_stem, cons_root, ):
    X_leaf: float = 0
    X_root: float = 0
    X_stem: float = 0
    Y_root: float = 0
    Y_stem: float = 0
    Z_leaf: float = 0
    Z_stem: float = 0

    computeInitialLeafBiomass()
