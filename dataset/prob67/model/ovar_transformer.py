def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms output dictionary into the format expected by the reference model.

    Args:
        ovar_dict (dict): Dictionary containing 'grid' key.
    
    Returns:
        dict: Dictionary with key 'x' mapped to the 2D array.
    """
    return {"x": ovar_dict["grid"]}
