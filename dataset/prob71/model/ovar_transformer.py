def ovar_transformer(ovar_dict, param_dict=None):
    """
    Pass-through transformer for binary puzzle output.

    Args:
        ovar_dict (dict): Should contain 'grid': List[List[int]] of size [n][n]

    Returns:
        dict: {'x': grid} directly usable by the reference model
    """
    return {"x": ovar_dict["grid"]}
