def ovar_transformer(ovar_dict, param_dict):
    """
    For the 'fraction sum to 1' cryptarithmetic puzzle, return 'vars' as is.

    Args:
        ovar_dict: dict with 'vars': List[int]
        param_dict: dict (not used)

    Returns:
        dict: {'Vars': List[int]}
    """
    return {"Vars": ovar_dict["vars"]}
