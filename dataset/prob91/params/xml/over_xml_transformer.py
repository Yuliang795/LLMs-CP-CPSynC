def ovar_transformer(ovar_dict, param_dict=None):
    """
    Convert lineup (order left->right) into positions per friend.

    Input:
      ovar_dict = {
        "lineup": List[int],  # permutation of [0..6]
        "unsatisfied": int    # optional: number of unmet adjacency prefs
      }

    Output (to bind in the model):
      {
        "friends": List[int],  # positions: friends[i] = position of friend i
        "z": int (optional)    # equals 'unsatisfied' if you add an aux var
      }
    """
    lineup = ovar_dict["lineup"]
    n = len(lineup)
    positions = [None] * n  # friends[i] = index where i appears in lineup
    for pos, person in enumerate(lineup):
        positions[person] = pos

    out = {"friends": positions}
    if "unsatisfied" in ovar_dict:
        out["z"] = ovar_dict["unsatisfied"]
    return out
