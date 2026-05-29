def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the output variables into a dict usable for model injection/validation.

    Args:
        ovar_dict (dict): Output format containing:
            - "assignments": List[List[int]], shape = [nPieces][nItems]
            - "num_pieces": int

    Returns:
        dict: With keys aligned to decision variables in the reference model.
              {'r': ..., 'p': ...}
    """
    assignments = ovar_dict["assignments"]
    num_pieces = ovar_dict["num_pieces"]
    nPieces = param_dict['N']
    nItems = param_dict['nItems']

    # Convert to CSP variable format
    r = assignments
    p = [int(any(assignments[i])) for i in range(nPieces)]  # used if any item is cut

    return {"r": r, "p": p, "z": num_pieces}
