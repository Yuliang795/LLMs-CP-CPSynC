def ovar_transformer(ovar_dict, param_dict):
    """
    For the maximum clique problem, map 'c' and 'size' directly.

    Args:
        ovar_dict: dict with 'c': List[int], 'size': int
        param_dict: dict (not used)

    Returns:
        dict: {'c': List[int], 'size': int}
    """
    return {
        "c": [bool(x) for x in ovar_dict["c"]],
        "size": ovar_dict["size"]
    }
