def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps generated output 'labels' and 'cyclic_bandwidth' to reference model variables 'x' and 'z'.
    Args:
        ovar_dict: dict with keys 'labels' and 'cyclic_bandwidth'
    Returns:
        dict: with keys 'x', 'z'
    """
    result = {"x": ovar_dict["labels"]}
    result["z"] = ovar_dict["cyclic_bandwidth"]
    return result
