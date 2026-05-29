def ovar_transformer(ovar_dict, param_dict):
    """
    For the traffic junction problem, directly return the arrays V and P.

    Args:
        ovar_dict: dict with 'V': List[int], 'P': List[int]
        param_dict: dict (not used)

    Returns:
        dict: {'V': List[int], 'P': List[int]}
    """
    return {
        "V": ovar_dict["V"],
        "P": ovar_dict["P"]
    }
