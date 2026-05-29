def ovar_transformer(ovar_dict, param_dict):
    """
    Transforms the Nonogram output 'grid' into the reference model variable 'x'.

    Args:
        ovar_dict: dict with 'grid': List[List[int]], 0=unshaded, 1=shaded
        param_dict: dict with 'rows', 'cols'

    Returns:
        dict: {'x': List[List[int]]}, with MiniZinc's value encoding (1=shaded, 2=unshaded)
    """
    grid = ovar_dict["grid"]
    # Map 1 -> 1 (shaded), 0 -> 2 (unshaded)
    x = [
        [1 if cell == 0 else 2 for cell in row]
        for row in grid
    ]
    return {"x": x}
