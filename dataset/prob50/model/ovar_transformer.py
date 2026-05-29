def ovar_transformer(ovar_dict, param_dicm=None):
    """
    Map 'edge_colors' (1-based, n x n) to reference model 'x' (0-based, for i<j), and num_colors to 'z' (max color index used).
    Args:
        ovar_dict: dict with keys 'edge_colors' and 'num_colors'
    Returns:
        dict: with keys 'x', 'z'
    """
    edge_colors = ovar_dict["edge_colors"]
    n = len(edge_colors)
    # Only fill x[i][j] for i<j
    x = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i < j:
                x[i][j] = edge_colors[i][j] - 1
    # Objective variable z (optional, if you wish to verify)
    z = ovar_dict["num_colors"] -1

    return {"x": x, "z": z}
    