def ovar_transformer(ovar_dict, param_dict=None):
    """
  
    Returns:
        dict: with key 'x' and 'z', no change needed
    """
    result = {"x": ovar_dict["bids"]}
    result["z"] = ovar_dict["total_value"]
    return result
