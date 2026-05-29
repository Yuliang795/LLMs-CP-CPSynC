def ovar_transformer(ovar_dict, param_dict):
    """
    For the sum-triple balls-in-boxes problem, directly returns the solution in reference model format.

    Args:
        ovar_dict: dict with 'box': List[int]
        param_dict: dict with 'n', 'c' (not needed for this transformation)

    Returns:
        dict: {'box': List[int]}
    """
    return {"box": ovar_dict["box"]}
