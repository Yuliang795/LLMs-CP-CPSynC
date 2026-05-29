def ovar_transformer(ovar_dict, param_dict):
    """
    For the bus driver scheduling/set partitioning problem, map 'total_shifts' to 'tot_shifts' and keep 'x' as is.

    Args:
        ovar_dict: dict with 'total_shifts': int, 'x': List[int]
        param_dict: dict (not used)

    Returns:
        dict: {'tot_shifts': int, 'x': List[int]}
    """
    return {
        "tot_shifts": ovar_dict["total_shifts"],
        "x": ovar_dict["x"]
    }
