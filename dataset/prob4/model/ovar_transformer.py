def ovar_transformer(ovar_dict, param_dict):
    """
    For the Golomb ruler problem, directly returns the marks in the reference model format.

    Args:
        ovar_dict: dict with 'mark': List[int]
        param_dict: dict (contains 'm', optional)

    Returns:
        dict: {'mark': List[int]}
    """
    return {"mark": ovar_dict["mark"], "z":ovar_dict["mark"][-1]}
