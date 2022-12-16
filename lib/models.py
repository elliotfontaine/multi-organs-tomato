import cobra

def createOrganModel(default_model: cobra.Model, organ_cons) -> cobra.Model:
    organ_model = default_model.copy()
    organ_model.objective = {
        organ_model.reactions.get_by_id(organ_cons['obj'][0]['reac']): organ_cons['obj'][0]['coeff']
    }
    organ_model.objective.direction = organ_cons['obj'][0]['direction']
    for flux in organ_cons['flux']:
        organ_model.reactions.get_by_id(flux['reac']).bounds = (
            flux['minbound'],
            flux['maxbound']
        )
    return organ_model

def updateModelConstraints(
        model: cobra.Model, reactions_constraints: list) -> None:
    for cons in reactions_constraints:
        model.reactions.get_by_id(cons[0]).bounds = (cons[1], cons[1])