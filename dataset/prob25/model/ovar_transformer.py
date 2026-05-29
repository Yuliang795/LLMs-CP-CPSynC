def ovar_transformer(ovar_dict, param_dict):
    """
    For the graceful labelling problem, directly map nodes and edges.

    Args:
        ovar_dict: dict with 'nodes': List[int], 'edges': List[int]
        param_dict: dict (not used)

    Returns:
        dict: {'nodes': List[int], 'edges': List[int]}
    """
    return {
        "nodes": ovar_dict["nodes"],
        "edges": ovar_dict["edges"]
    }
