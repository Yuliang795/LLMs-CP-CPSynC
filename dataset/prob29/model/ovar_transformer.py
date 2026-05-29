def ovar_transformer(ovar_dict, param_dict):
    """
    For the quasigroup (Latin square completion) problem, map 'puzzle' directly.

    Args:
        ovar_dict: dict with 'puzzle': List[List[int]]
        param_dict: dict (not used)

    Returns:
        dict: {'puzzle': List[List[int]]}
    """
    return {"puzzle": ovar_dict["puzzle"]}
