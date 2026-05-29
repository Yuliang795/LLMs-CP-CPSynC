def ovar_transformer(ovar_dict, param_dict):
    """
    For the all-interval series problem, directly returns the series in the reference model format.

    Args:
        ovar_dict: dict with 'series': List[int]
        param_dict: dict (contains 'n', optional)

    Returns:
        dict: {'series': List[int]}
    """
    return {"series": ovar_dict["series"]}
