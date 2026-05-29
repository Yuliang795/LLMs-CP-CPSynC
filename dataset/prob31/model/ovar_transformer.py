def ovar_transformer(ovar_dict, param_dict=None):
    """
    Returns:
        list: mapping to keys 'c1', 'c5', 'c10', 'c20', 'c50', 'e1', 'e2', no change needed
    """
    return {'coins': ovar_dict['coins']}