def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps the generated solution to the reference model variables.

    Args:
        ovar_dict: dict with keys:
          - "m": int, number of men
          - "w": int, number of women
          - "c": int, number of children

    Returns:
        dict: {"m": m, "w": w, "c": c}
    """
    return {
        "m": ovar_dict["m"],
        "w": ovar_dict["w"],
        "c": ovar_dict["c"],
    }
