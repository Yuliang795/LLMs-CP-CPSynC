def ovar_transformer(ovar_dict, param_dict):
    """
    For the magic square problem, map magic_sum to 's' and keep 'square' as-is.

    Args:
        ovar_dict: dict with 'magic_sum': int, 'square': List[List[int]]
        param_dict: dict (not used)

    Returns:
        dict: {'s': int, 'square': List[List[int]]}
    """
    return {
        "s": ovar_dict["magic_sum"],
        "square": ovar_dict["square"]
    }
