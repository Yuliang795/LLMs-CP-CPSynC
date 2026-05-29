def ovar_transformer(ovar_dict, param_dict):
    """
    For the Langford/L(k,n) sequence problem, return the solution list as is.

    Args:
        ovar_dict: dict with 'solution': List[int]
        param_dict: dict (not used)

    Returns:
        dict: {'solution': List[int]}
    """
    return {"solution": ovar_dict["solution"]}
