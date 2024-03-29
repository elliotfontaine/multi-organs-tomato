import cobra

import pandas as pd
import os
import lib.io
import lib.fba
import lib.models

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# CONSTANTS
CONFIG = lib.io.loadConfig('input/config.yaml')
COBRA_CONFIG = lib.io.editCobraConfig(cobra.Configuration(), CONFIG)
XYLEM_NUTRIENTS = tuple(CONFIG['xylem_nutrients'])
ORGANS = ('leaf', 'stem', 'root') # Can't be changed easely for now 😢


def main():
    biomasses: dict = {organ: float for organ in ORGANS}
    time_series_biomass: dict = {organ: [] for organ in ORGANS}
    fba_flux: dict = {organ: pd.DataFrame for organ in ORGANS}
    leaf_xylem: dict = {nutrient: float for (nutrient) in XYLEM_NUTRIENTS}
    stem_xylem: dict = {nutrient: float for (nutrient) in XYLEM_NUTRIENTS}
    root_soil: dict = {nutrient: float for (nutrient) in XYLEM_NUTRIENTS}
    stem_sucr: float
    root_sucr: float
    
    # Create a default plant model from sbml file written in config.yml
    default_model = cobra.io.read_sbml_model(CONFIG['paths']['sbml'])
    models = {'default': default_model}
    
    # Duplicate the model 3* (leaf, stem and root models)
    for organ in (ORGANS):
        cons_file = CONFIG['paths']['organs_constraints'].get(organ)
        organ_cons = lib.io.parseConstraintsFile(cons_file)
        models[organ] = lib.models.createOrganModel(default_model, organ_cons)
    
    # We actually force the models objectives for the loop, even if the
    # constraints file parser actually process the objectives
    # (it should then be reusable in another Python project).
    for sink_organ in ('stem', 'root'):
        models[sink_organ].objective = CONFIG['sucrose_ex_reac']
        models[sink_organ].objective.direction = 'max'
    models['leaf'].objective = CONFIG['biomass_reac']['leaf']
    models[sink_organ].objective.direction = 'max'
    
    # Add nutrients export reactions in root model, for leaf/stem supply
    for nutrient in XYLEM_NUTRIENTS:
        # print(models['root'].reactions.get_by_id(f'EX_{nutrient}_eb'))
        export_reac: cobra.Reaction = models['root'].reactions.get_by_id(
            f'EX_{nutrient}_eb').copy()
        export_reac.id = f'EXPORT_{nutrient}_cb'
        export_reac.name = f'{nutrient} export from root to xylem'
        export_reac.bounds = (0., 1000.)
        models['root'].add_reactions([export_reac])
        # print(models['root'].reactions.get_by_id(export_reac.id))
    models['root'].repair()
        
    loops = 0
    while (not hasConverged(time_series_biomass)
           and loops <= CONFIG['max_loop_number']):
        leaf_biomass, leaf_xylem, fba_flux['leaf'] \
            = lib.fba.leafFba(models['leaf'],
                              leaf_xylem,
                              CONFIG['biomass_reac']['leaf']
        )
        updateBiomasses(leaf_biomass, biomasses, time_series_biomass, CONFIG)
        stem_new_constraints = [(CONFIG['biomass_reac']['stem'],
                                 biomasses['stem'])]
        lib.models.updateModelConstraints(models['stem'], stem_new_constraints)
        stem_sucr, stem_xylem, fba_flux['stem'] = \
            lib.fba.sinkFba(models['stem'],
                            stem_xylem,
                            CONFIG['sucrose_ex_reac'])
        root_new_constraints = [
            (f'EXPORT_{nutrient}_cb',
             -(
                 leaf_xylem[nutrient]*CONFIG['dry_weight_ratios']['leaf/root']
                 + stem_xylem[nutrient]*CONFIG['dry_weight_ratios']['stem/root']))
            for nutrient in XYLEM_NUTRIENTS
        ] + [(CONFIG['biomass_reac']['root'], biomasses['root'])]
        lib.models.updateModelConstraints(models['root'], root_new_constraints)
        root_sucr, root_soil, fba_flux['root'] = \
            lib.fba.sinkFba(models['root'],
                            root_soil,
                            CONFIG['sucrose_ex_reac'])
        leaf_new_constraints = [
            (CONFIG['sucrose_ex_reac'],
            -(
                stem_sucr/CONFIG['dry_weight_ratios']['leaf/stem']
                + root_sucr/CONFIG['dry_weight_ratios']['leaf/root']))
        ]
        lib.models.updateModelConstraints(models['leaf'], leaf_new_constraints)
        loops += 1
        print(f"loop: {loops} ")
        
    print(time_series_biomass)
    print(f'{loops} loops before convergence.')
    lib.io.drawTimeSeries(time_series_biomass,
                          'Biomasses time series',
                          'output/biomasses_plot.png')
    for organ in ORGANS:
        lib.io.writeFbaFluxTable(fba_flux[organ], 
                                 f'output/{organ}_fba_results.tsv')


def updateBiomasses(leaf_biomass, dict_biomasses, dict_series, config) -> None:
    biomass_rates = config['biomass_rates']
    dict_biomasses['leaf'] = leaf_biomass
    dict_biomasses['stem'] = leaf_biomass*(biomass_rates['stem']/
                                           biomass_rates['leaf'])
    dict_biomasses['root'] = leaf_biomass*(biomass_rates['root']/
                                           biomass_rates['leaf'])
    for organ in dict_biomasses:
        dict_series[organ].append(dict_biomasses[organ])

     
def hasConverged(time_series_biomass):
    if len(time_series_biomass['leaf']) < 2:
        return False
    t = time_series_biomass['leaf'][-1]
    t_minus_1 = time_series_biomass['leaf'][-2]
    deviation = abs(t-t_minus_1)/t
    return deviation < CONFIG['convergence_threshold']

main()