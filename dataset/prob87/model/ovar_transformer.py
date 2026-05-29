def ovar_transformer(ovar_dict, param_dict=None):
    """
    Map the solver's output to the reference model variables.

    Args:
        ovar_dict: dict with keys:
          - "tour": List[int] of length n (order of cities; the tour returns to tour[0] implicitly)
          - "z"   : int, total tour length (optional for verification)

    Returns:
        dict with keys matching the reference model:
          - 'c': the city order
          - 'z': (optional) total length, if provided
    """
    res = {"c": ovar_dict["tour"]}
    res["z"] = ovar_dict["z"]
    return res
