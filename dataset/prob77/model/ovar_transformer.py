def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the provided grid (with 0 for black cells) into the reference
    model's decision variable dictionary.

    Args:
        ovar_dict (dict): {
            "grid": List[List[int]]
        }

    Returns:
        dict: {"x": grid_with_None_for_black}
    """
    grid = ovar_dict["grid"]
    

    return {"x": grid}
