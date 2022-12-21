import cobra
from lib.io import Constraints


# Should probably be a subclass of cobra.Model, and the function be a method.

def createOrganModel(default_model: cobra.Model,
                     organ_cons: Constraints) -> cobra.Model:
    
    organ_model = default_model.copy()
    
    # Specify objective
    organ_model.objective = {
        organ_model.reactions.get_by_id(
            organ_cons['obj'][0]['reac']): organ_cons['obj'][0]['coeff']
    }
    organ_model.objective.direction = organ_cons['obj'][0]['direction']
    
    # Specify bounds
    for flux in organ_cons['flux']:
        organ_model.reactions.get_by_id(flux['reac']).bounds = (
            flux['minbound'],
            flux['maxbound']
        )
    
    # Specify equations
    equations = organ_cons['equations']
    for equation in equations:
        coefficients = dict()
        for idx, reac_id in enumerate(equation['left_reacs']):
            reac = organ_model.reactions.get_by_id(reac_id)
            coefficients[reac.forward_variable] = equation['left_coeffs'][idx]
            coefficients[reac.reverse_variable] = equation['left_coeffs'][idx]
        for idx, reac_id in enumerate(equation['right_reacs']):
            reac = organ_model.reactions.get_by_id(reac_id)
            coefficients[reac.forward_variable] = -equation['right_coeffs'][idx]
            coefficients[reac.reverse_variable] = -equation['right_coeffs'][idx]
        constraint = organ_model.problem.Constraint(0, lb=0, ub=0)
        organ_model.add_cons_vars(constraint)
        organ_model.solver.update()
        constraint.set_linear_coefficients(coefficients=coefficients)
    return organ_model


def updateModelConstraints(
        model: cobra.Model, reactions_constraints: list) -> None:
    for cons in reactions_constraints:
        model.reactions.get_by_id(cons[0]).bounds = (cons[1], cons[1])