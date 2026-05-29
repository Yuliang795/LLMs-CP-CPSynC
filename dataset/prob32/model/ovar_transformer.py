def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the generated 'colors' output (1-indexed) to the reference model's 'x' (0-indexed).
    
    Returns:
        dict: with key 'x', value is the 0-based color array
    """
    colors = ovar_dict["colors"]
    x = [[v - 1 for v in row] for row in colors]
    z = max(max(row) for row in x)

    return {"x": x, 'z':z}
