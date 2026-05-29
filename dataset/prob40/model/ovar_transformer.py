def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the output solution dict (with 'tour') to the reference model's variable format ('x').
    Args:
        ovar_dict: dict, contains key 'tour' with a 2D list of ints (the knight's tour solution)
    Returns:
        dict: with key 'x', value is a list where x[step] = cell index (row-major order)
    """
    tour = ovar_dict["tour"]
    n = len(tour)
    x = [None] * (n * n)
    for i in range(n):
        for j in range(n):
            step = tour[i][j]
            cell_index = i * n + j
            x[step] = cell_index
    return {"x": x}
