def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms generated output into variables for the reference model.
    Args:
        ovar_dict (dict): Should contain key 'grid'.
    Returns:
        dict: {'x': ...}
    """
    return {"x": ovar_dict["grid"]}
