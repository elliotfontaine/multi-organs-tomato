import cobra
from typing import Tuple

def computeBiomass(model: cobra.Model):
    return model.slim_optimize()

def leafFba(leaf_model: cobra.Model, 
            nutrients: dict, 
            objective: str) -> Tuple[int, dict]:
    fba_solution = cobra.flux_analysis.pfba(leaf_model)
    biomass_leaf = fba_solution.fluxes[objective]
    flux_nutrients: dict = {}
    for nutrient in nutrients:
        flux_nutrients[nutrient] = fba_solution.fluxes[f'EX_{nutrient}_eb']
    return(biomass_leaf, flux_nutrients, fba_solution.fluxes)

def sinkFba(sink_model: cobra.Model,
            nutrients: dict,
            objective: str) -> Tuple[int, dict]:
    fba_solution = cobra.flux_analysis.pfba(sink_model)
    flux_sucrose = fba_solution.fluxes[objective]
    flux_nutrients = {}
    for nutrient in nutrients:
        flux_nutrients[nutrient] = fba_solution.fluxes[f'EX_{nutrient}_eb']
    return(flux_sucrose, flux_nutrients, fba_solution.fluxes)
