def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps generated output 'locs' to reference model variables 'x' and 'y'.
    Args:
        ovar_dict: dict with key 'locs'
    Returns:
        dict: with keys 'x', 'y'
    """
    locs = ovar_dict["locs"]
    x = [loc[0] for loc in locs]
    y = [loc[1] for loc in locs]
    return {"x": x, "y": y}
