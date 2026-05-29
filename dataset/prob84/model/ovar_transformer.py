def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps the generated 'grid' (n x n integers 1..n) to the reference model's variable 'x'.
    """
    return {"x": ovar_dict["grid"]}
