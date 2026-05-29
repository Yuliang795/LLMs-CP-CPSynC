def ovar_transformer(ovar_dict, param_dict=None):
    """
    Returns:
        dict: 'x': value is the grid, no change needed
              'z': value is the obj computed as the sum of x[i][j] * (i-j)^2
    """
    grid = ovar_dict["grid"]
    n = param_dict["n"] if param_dict and "n" in param_dict else len(grid)
    # Compute objective value: sum of x[i][j] * (i-j)^2
    z = sum(
        grid[i][j] * (i - j) ** 2
        for i in range(n) for j in range(n)
    )
    return {"x": grid, "z": z}