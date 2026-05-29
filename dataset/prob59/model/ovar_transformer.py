def ovar_transformer(ovar_dict, param_dict=None):
    """
   
    Returns:
        dict: with key 'v' (and 'z' if cost present)
    """
    result = {"v": ovar_dict["voucher_usage"]}
    
    result["z"] = ovar_dict["cost"]
    return result
