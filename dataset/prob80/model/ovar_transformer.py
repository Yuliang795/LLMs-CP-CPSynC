def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transform the solver's 'grid' output into the reference model's
    decision variable mapping.

    Args:
        ovar_dict (dict): {
            "grid": List[List[int]]
        }

    Returns:
        dict: {"x": grid}
              where x[i][j] is 0/1 for blanks and always 0 for clue cells
    """
    grid = ovar_dict["grid"]

    # In this case, output grid is already consistent with x:
    # - Clue cells are 0
    # - Blank cells are 0 or 1
    return {"x": grid}
