def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the generated 'grid' and 'army_size' to the reference model's 'b', 'w' variables.
    Args:
        ovar_dict: dict with keys 'grid' (2D list) and 'army_size' (int)
    Returns:
        dict: keys 'b', 'w', and 'army_size'
    """
    grid = ovar_dict["grid"]
    n = len(grid)
    b = []
    w = []
    for i in range(n):
        row_b = []
        row_w = []
        for j in range(n):
            if grid[i][j] == 1:
                row_b.append(1)
                row_w.append(0)
            elif grid[i][j] == 2:
                row_b.append(0)
                row_w.append(1)
            else:
                row_b.append(0)
                row_w.append(0)
        b.append(row_b)
        w.append(row_w)
    return {
        "b": b,
        "w": w,
        "army_size": ovar_dict["army_size"]
    }
