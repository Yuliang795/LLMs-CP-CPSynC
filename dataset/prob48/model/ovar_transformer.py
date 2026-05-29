def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms 'coloring' output to the reference model's variable 'x'.
    Args:
        ovar_dict: dict, key 'coloring' (list of length n)
    Returns:
        dict: with key 'x', value is a list of length n+1 (x[0]=0)
    """
    coloring = ovar_dict["coloring"]
    x = [0] + coloring
    return {"x": x}
