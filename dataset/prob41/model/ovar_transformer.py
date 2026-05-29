def ovar_transformer(ovar_dict, param_dict=None):
    """
  
    Returns:
        dict: with key 'x' (list of ints), and 'z' (int, objective)
    """
    return {
        "x": ovar_dict["sequence"],
        "z": ovar_dict["energy"]  # Optional, if you include an explicit variable for the objective
    }
