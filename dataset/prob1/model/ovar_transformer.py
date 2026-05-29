def ovar_transformer(ovar_dict, param_dict):
    """
    Transforms output solution to reference model decision variable format.
    Only includes 'slot' as that's sufficient for validation.
    """
    slot = ovar_dict["slot"]
    if min(slot)==0:
        slot = [s + 1 for s in slot]
    return {
        "slot": slot
    }
