import cobra
from lib.io import *
from lib.fba import *


leaf_biomass: float = 0
root_biomass: float = 0
stem_biomass: float = 0
leaf_biomass_list: list = []
root_biomass_list: list = []
stem_biomass_list: list = []
root_phloem: dict = {'sucr': float}
stem_phloem: dict = {'sucr': float}
leaf_xylem: dict = {'no3': float, '...' : float}
stem_xylem: dict = {'no3': float, '...' : float}

def createOrganModel(default_model, organ_cons):
    organ_model = default_model.copy()
    organ_model.objective = organ_cons['obj'][0]['reac']
    organ_model.objective.direction = organ_cons['obj'][0]['direction']
    for flux in organ_cons['flux']:
        organ_model.reactions.get_by_id(flux['reac']).bounds = (flux['minbound'], flux['maxbound'])
    return organ_model


def main():
    config = loadConfig('input/config.yaml')
    cobra_config = cobra.Configuration()
    default_model = cobra.io.read_sbml_model(config['paths']['sbml'])
    models = {'default': default_model}
    for organ in ('leaf', 'stem', 'root'):
        cons_file = config['paths']['organ_constraints'].get(organ)
        organ_cons = parseConstraintsFile(cons_file)
        models['organ'] = createOrganModel(default_model, organ_cons)
    print(models)
    
    # leaf_biomass = computeInitialLeafBiomass()
    # updateBiomasses(leaf_biomass) # change les biomasses des 2 autres, et ajoute aux 3 listes
    
    # solution = leaf_model.optimize()
    # print(solution)

print(parseConstraintsFile('input/constraints_tomato_day.txt'))