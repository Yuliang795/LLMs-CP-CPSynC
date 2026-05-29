def ovar_transformer(ovar_dict, param_dict=None):
    """
    Returns:
        dict: with key 'x' (list of lists), and optionally 'z' for num_treaties
    """
    treaty_matrix = ovar_dict["treaty_matrix"]
    n = len(treaty_matrix)
    x = []
    for i in range(n):
        row = []
        for j in range(n):
            if i < j:
                row.append(treaty_matrix[i][j])
            else:
                row.append(None)
        x.append(row)
    result = {"x": x}
    result["z"] = ovar_dict["num_treaties"]
    return result
