def ovar_transformer(ovar_dict, param_dict=None):
    """
  
    Returns:
        dict: with key 'x' and 'z' 
    """
    result = {"x": ovar_dict["successors"]}
    
    result["z"] = ovar_dict["benefit"]
    return result
