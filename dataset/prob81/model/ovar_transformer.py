def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transform placements output into reference model variables (x, y).
    
    Args:
        ovar_dict (dict): {
            "placements": List[List[int]]
        }
        
    Returns:
        dict: {"x": [...], "y": [...]}
    """
    placements = ovar_dict["placements"]
    
    x = [p[0] for p in placements]
    y = [p[1] for p in placements]
    
    return {"x": x, "y": y}
