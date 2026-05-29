def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the output dictionary into the variable dict required by the reference model.

    Args:
        ovar_dict (dict): Dictionary containing key 'grid'.

    Returns:
        dict: Dictionary with model variable key 'x'.
    """
    return {"x": ovar_dict["grid"]}
