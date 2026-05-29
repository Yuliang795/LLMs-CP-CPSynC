def ovar_transformer(ovar_dict, param_dict=None):
    """
    Returns:
        dict: with keys 'x', 'y' for the latin squares, no change needed
    """
    return {
        "x": ovar_dict["latin_square_1"],
        "y": ovar_dict["latin_square_2"]
    }
