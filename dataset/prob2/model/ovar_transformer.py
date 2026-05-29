def ovar_transformer(ovar_dict, param_dict):
    """
    Transform solution output into reference model's decision variable format.

    Args:
        ovar_dict: dict with keys 'template' (List[List[int]]) and 'pressings' (List[int])
        param_dict: dict, problem parameters (not needed for this transformation)
    
    Returns:
        dict with:
            - 'p': List[List[int]], shape [n][t], p[i][j] = slots of variation i in template j
            - 'R': List[int], length t, R[j] = pressings of template j
    """
    template = ovar_dict["template"]      # [t][n]
    pressings = ovar_dict["pressings"]    # [t]

    # Transpose template to get [n][t] for 'p'
    # template[j][i] => p[i][j]
    # template: rows = templates, columns = variations
    # p: rows = variations, columns = templates
    p = [ [template[j][i] for j in range(len(template))] 
          for i in range(len(template[0])) ]   # [n][t]

    R = pressings

    return {
        "p": p,    # [n][t]
        "R": R,     # [t]
        "Production": sum(R)  # Total pressings
    }
