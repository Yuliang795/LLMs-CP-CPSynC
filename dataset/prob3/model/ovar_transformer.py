def ovar_transformer(ovar_dict, param_dict):
    """
    For QG3.m quasigroup problems, directly returns the solution in reference model format.

    Args:
        ovar_dict: dict with 'quasiGroup': List[List[int]]
        param_dict: dict with at least 'n': int

    Returns:
        dict: {'quasiGroup': List[List[int]]}
    """
    return {"quasiGroup": ovar_dict["quasiGroup"]}
