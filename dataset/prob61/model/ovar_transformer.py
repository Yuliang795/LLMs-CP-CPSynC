def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps generated output to reference model variables for TSPTW.
    Args:
        ovar_dict: dict with keys 'tour', 'service_times', 'distance'
    Returns:
        dict: keys 'x', 'a', and optionally 'z'
    """
    result = {
        "x": ovar_dict["tour"],
        "a": ovar_dict["service_times"],
    }
    result["z"] = ovar_dict["distance"]
    return result
