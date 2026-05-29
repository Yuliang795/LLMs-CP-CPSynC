def ovar_transformer(ovar_dict, param_dict=None):
    """
    Map the generated 2D assignment 'grid' to the reference model variable 'x'.
    Args:
        ovar_dict (dict): must contain key 'grid' -> List[List[int]] of shape [m][n]
    Returns:
        dict: {'x': grid}
    """
    return {"x": ovar_dict["grid"]}
