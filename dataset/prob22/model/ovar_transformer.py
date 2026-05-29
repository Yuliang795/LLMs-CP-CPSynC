def ovar_transformer(ovar_dict, param_dict):
    """
    For the ternary Steiner system, sort each triple and rename to Sets.

    Args:
        ovar_dict: dict with 'sets': List[List[int]]
        param_dict: dict (not used)

    Returns:
        dict: {'Sets': List[List[int]]}
    """
    sets = [set(sorted(triple)) for triple in ovar_dict["sets"]]
    return {"Sets": sets}
