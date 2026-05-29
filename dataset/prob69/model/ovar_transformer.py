def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the output grid into the circuit variable x.

    Args:
        ovar_dict (dict): Should contain the key 'grid' with a 10x10 2D array.

    Returns:
        dict: {'x': List[int]} to match the circuit variable in the model.
    """
    grid = ovar_dict["grid"]
    n = param_dict['n']
    n2 = n * n

    # Create a map from step number to cell index
    step_to_index = [0] * n2
    for i in range(n):
        for j in range(n):
            t = grid[i][j]
            step_to_index[t] = i * n + j

    # Build successor array
    x = [0] * n2
    for t in range(n2 - 1):
        curr = step_to_index[t]
        next_ = step_to_index[t + 1]
        x[curr] = next_
    x[step_to_index[n2 - 1]] = step_to_index[0]  # close the circuit

    return {"x": x}
