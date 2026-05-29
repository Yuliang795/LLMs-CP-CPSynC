def ovar_transformer(ovar_dict, param_dict):
    """
    Transform generated output ('min_moves', 'moves') to the reference model variable format:
    - 'z': the minimal number of moves
    - 'y': the list of cookies eaten at each step
    - 'x': the state of the jars after each step
    Args:
        ovar_dict: dict, keys 'min_moves' and 'moves'
    Returns:
        dict with keys 'z', 'y', 'x'
    """
    min_moves = ovar_dict["min_moves"]
    moves = ovar_dict["moves"]
    # Infer the number of jars
    if not moves:
        raise ValueError("No moves found.")
    # If moves is empty, this means all jars are initially empty, handle edge case
    nJars = max((max(m['jars']) if m['jars'] else -1) for m in moves) + 1 if moves else 0
    # Try to recover initial state from a separate data variable (as in pycsp3 reference)
    jars = param_dict.get("cookies")  # Optionally supply in ovar_dict
    if jars is None:
        raise ValueError("Initial jars state must be provided in ovar_dict['jars']")
    horizon = len(jars) + 1

    # Construct y (length = horizon)
    y = [0] * horizon
    for i, move in enumerate(moves):
        y[i] = move['amount']
    # Remaining entries after min_moves are 0 by default

    # Construct x
    x = [list(jars)]  # initial state
    current = list(jars)
    for i in range(min_moves):
        move = moves[i]
        amount = move['amount']
        jars_idxs = move['jars']
        next_state = current[:]
        for idx in jars_idxs:
            next_state[idx] -= amount
            if next_state[idx] < 0:
                raise ValueError(f"Negative cookies in jar {idx} after move {i}")
        x.append(next_state)
        current = next_state
    # Pad x to horizon length with same final state (all zeros)
    while len(x) < horizon:
        x.append([0]*len(jars))

    # z
    z = min_moves

    return {
        "x": x,
        "y": y,
        "z": z
    }
