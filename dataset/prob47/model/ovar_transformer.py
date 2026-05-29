def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms 'board' and 'max_pennies' output to reference variables: p, x, y, xy.
    Args:
        ovar_dict: dict with 'board' and 'max_pennies'
    Returns:
        dict: with keys 'p', 'x', 'y', 'xy'
    """
    board = ovar_dict["board"]
    n = param_dict["n"]
    penny_positions = [(i, j) for i in range(n) for j in range(n) if board[i][j] == 1]
    max_pennies = ovar_dict["max_pennies"]
    # Sort penny_positions lex order to be consistent
    penny_positions.sort()
    p = [1]*len(penny_positions) + [0]*(n - len(penny_positions))
    x = [i for (i, j) in penny_positions] + [-1]*(n - len(penny_positions))
    y = [j for (i, j) in penny_positions] + [-1]*(n - len(penny_positions))
    xy = [i*n + j for (i, j) in penny_positions] + [-1]*(n - len(penny_positions))
    return {"p": p, "x": x, "y": y, "xy": xy}
