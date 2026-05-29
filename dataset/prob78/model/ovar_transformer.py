def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the solver output (selected items, total value)
    into reference model variable mapping.

    Args:
        ovar_dict (dict): {
            "selected": List[int],
            "total_value": int
        }

    Returns:
        dict: {"x": ..., "z": ...}
              where x is the selection vector, z is the objective value
    """
    return {
        "x": ovar_dict["selected"],
        "z": ovar_dict["total_value"]
    }
