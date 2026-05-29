def compute_z_from_x(x, q):
    z = [0] * q
    for row in x:
        for cell in row:
            if 1 <= cell <= q:
                z[cell-1] += 1
    return z

def ovar_transformer(ovar_dict, param_dict):
    """
    "board" as a 2D list [n][n], where board[i][j] is 0 (empty) or 1..q (queen color)
    Returns:
        x: 2D list [n][n], no change needed
    """
    x = ovar_dict["board"]
    z = compute_z_from_x(x, param_dict['q'])
    return {"x": x, "z": z}
