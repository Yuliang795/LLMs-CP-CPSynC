def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the provided path + total_gold into the reference model's
    decision variables {s, z}.

    Args:
        ovar_dict (dict): {
            "path": List[int],
            "total_gold": int
        }
        nHouses (int): number of houses in the graph

    Returns:
        dict: {"s": ..., "z": ...}
              where s is the successor array (reference model format),
              z is the total gold collected.
    """
    path = ovar_dict["path"]
    total_gold = ovar_dict["total_gold"]

    # initialize all successors as "self" (not part of path)
    s = list(range(param_dict["nHouses"]))

    # set successors for path nodes
    for i in range(len(path) - 1):
        s[path[i]] = path[i + 1]

    # enforce Luigi → Mario to close circuit
    s[path[-1]] = path[0]

    return {
        "s": s,
        "z": total_gold
    }
