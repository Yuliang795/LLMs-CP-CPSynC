def ovar_transformer(ovar_dict, param_dict=None):
    """
   
    Returns:
        dict: with key 'x' for the grid and 'z' for the grid sum, no change needed
    """
    return {
        "x": ovar_dict["grid"],
        "z": ovar_dict["grid_sum"]  # Optional, only if you define a z in the model
    }
