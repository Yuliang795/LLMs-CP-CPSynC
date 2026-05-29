def ovar_transformer(ovar_dict, param_dict=None):
    """
   
    Returns:
        dict: with key 'x' (2D list)
    """
    # x = [sorted(card) for card in ovar_dict["cards"]]
    # x = sorted(x)
    return {"x": ovar_dict["cards"]}
