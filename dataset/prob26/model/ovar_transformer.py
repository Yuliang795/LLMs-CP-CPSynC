def ovar_transformer(ovar_dict, param_dict):
    """
    For the n-queens problem, directly map queens.

    Args:
        ovar_dict: dict with 'queens': List[int]
        param_dict: dict (not used)

    Returns:
        dict: {'queens': List[int]}
    """
    return {"queens": ovar_dict["queens"]}
