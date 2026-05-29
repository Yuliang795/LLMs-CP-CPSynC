def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps 'grid' (n x n with 0 in upper triangle) to reference model 'x' (with None for i<j).
    Args:
        ovar_dict: dict with 'grid' and optionally 'max_nodes'
    Returns:
        dict: with key 'x' (lower triangle values, None elsewhere), and optionally 'z'
    """
    grid = ovar_dict["grid"]
    n = len(grid)
    x = []
    for i in range(n):
        row = []
        for j in range(n):
            if i >= j:
                row.append(grid[i][j])
            else:
                row.append(None)
        x.append(row)
    result = {"x": x}
    result["z"] = ovar_dict["max_nodes"]
    return result
