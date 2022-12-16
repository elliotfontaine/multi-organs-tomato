import cobra
from typing import Tuple

def computeBiomass(model: cobra.Model):
    return model.slim_optimize()

def leafFba(leaf_model: cobra.Model, nutrients: dict) -> Tuple[int, dict]:
    fba_solution = cobra.flux_analysis.pfba(leaf_model)
    biomass_leaf = fba_solution.fluxes['BIOMASS_LEAF_SLY_b'] # leaf_model.objective doesn't work because you can't get the objective function's name... Need a workaroud asap!
    flux_nutrients: dict = {}
    for nutrient in nutrients:
        flux_nutrients[nutrient] = fba_solution.fluxes[f'EX_{nutrient}_eb']
    return(biomass_leaf, flux_nutrients)

def sinkFba(sink_model: cobra.Model, nutrients: dict) -> Tuple[int, dict]:
    fba_solution = cobra.flux_analysis.pfba(sink_model)
    flux_sucrose = fba_solution.fluxes['EX_SUCR_eb'] # idem.
    flux_nutrients = {}
    for nutrient in nutrients:
        print(fba_solution.fluxes[f'EX_{nutrient}_eb'])
        flux_nutrients[nutrient] = fba_solution.fluxes[f'EX_{nutrient}_eb']
    return(flux_sucrose, flux_nutrients)

def computeRootSucrose(sbml, root_constraints, X_leaf, Z_leaf, Z_stem) -> float:
    pass

def computeStemSucrose(sbml, stem_constraints, X_leaf) -> float:
    pass
