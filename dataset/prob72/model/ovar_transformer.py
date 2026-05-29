def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms 'grid' into a format suitable for validation in the reference model.

    Args:
        ovar_dict (dict): Contains 'grid': List[List[int]] of size [n][n]

    Returns:
        dict: {'x': 2D grid of ints}
    """
    return {"x": ovar_dict["grid"]}
