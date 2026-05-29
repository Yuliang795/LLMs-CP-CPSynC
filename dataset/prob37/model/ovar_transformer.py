def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the generated 'grid' output to the reference variable 'x' format for Costas arrays.
    Args:
        ovar_dict: dict, contains key 'grid' with a 2D binary matrix [n][n]
    Returns:
        dict: with key 'x', where x[i] is the row of the mark in column i
    """
    grid = ovar_dict["grid"]
    n = param_dict["n"]
    #
    # check that the grid is valid: each row and column must contain exactly one mark (1)
    if any(sum(grid[i][j] for j in range(n)) != 1 for i in range(n)):
        raise ValueError("each row must contain exactly one mark")
    if any(sum(grid[i][j] for i in range(n)) != 1 for j in range(n)):
        raise ValueError("each column must contain exactly one mark")
    #
    x = []
    for j in range(n):
        # For each column, find the row index with a '1'
        for i in range(n):
            if grid[i][j] == 1:
                x.append(i)
                break
    return {"x": x}