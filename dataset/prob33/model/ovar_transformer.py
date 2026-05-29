def ovar_transformer(ovar_dict, param_dict=None):
    """
   
    Returns:
        dict with keys 'x', 'z', no change needed
    """
    return {
        "x": ovar_dict["arrangement"],
        "z": ovar_dict["max_r_sum"]
    }
