def ovar_transformer(ovar_dict, param_dict=None):
    """
    Returns:
        dict: with key 'x', no change needed
    """
    print(f"square: {ovar_dict['square']}")
    return {"x": ovar_dict["square"]}
