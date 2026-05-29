def ovar_transformer(ovar_dict, param_dict):
    """
    For the Killer Sudoku problem, directly map 'grid' to 'x'.

    Args:
        ovar_dict: dict with 'grid': List[List[int]]
        param_dict: dict (not used)

    Returns:
        dict: {'x': List[List[int]]}
    """
    return {"x": ovar_dict["grid"]}
