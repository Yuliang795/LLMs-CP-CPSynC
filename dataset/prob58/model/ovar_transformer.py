def ovar_transformer(ovar_dict, param_dict=None):
    """
   
    Returns:
        dict: keys 'depot', 'xa', 'xb', and 'z', no change needed
    """
    result = {
        "depot": ovar_dict["depot"],
        "xa": ovar_dict["tour_A"],
        "xb": ovar_dict["tour_B"]
    }
    result["z"] = ovar_dict["distance"]
    return result
