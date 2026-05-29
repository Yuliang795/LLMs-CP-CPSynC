def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms generated output back to reference model variables.
    
    Args:
        ovar_dict (dict): {
            "selected_arcs": List[List[int]],
            "total_weight": int
        }
        
    Returns:
        dict: {
            "a": selected arcs matrix,
            "z": total weight 
        }
    """
    selected_arcs = ovar_dict["selected_arcs"]
    total_weight = ovar_dict.get("total_weight", None)
    
    result = {"a": selected_arcs}
    result["z"] = total_weight
    return result
