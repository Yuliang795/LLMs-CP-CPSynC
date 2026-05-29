def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms 'board' and 'knight_cycle' output to reference variables: q and k.
    Args:
        ovar_dict: dict with 'board' and 'knight_cycle'
    Returns:
        dict: with keys 'q', 'k'
    """
    board = ovar_dict["board"]
    knight_cycle = ovar_dict["knight_cycle"]
    n = len(board)
    # Extract q
    q = []
    for i in range(n):
        for j in range(n):
            if board[i][j] in (1, 3):
                q.append(j)
                break
        else:
            raise ValueError(f"No queen found in row {i}")
    # Extract k
    k = []
    for row, col in knight_cycle:
        k.append(row * n + col)
    return {"q": q, "k": k}
