def ovar_transformer(ovar_dict, param_dict):
    """
    Transforms the output solution for the supply vessel loading problem to the reference model format.

    Args:
        ovar_dict: dict with 'left', 'right', 'bottom', 'top', 'orientation'
        param_dict: dict (not needed for transformation)

    Returns:
        dict: {'Left': ..., 'Right': ..., 'Bottom': ..., 'Top': ..., 'orientation': ...}
    """
    return {
        "Left": ovar_dict["left"],
        "Right": ovar_dict["right"],
        "Bottom": ovar_dict["bottom"],
        "Top": ovar_dict["top"],
        "orientation": ovar_dict["orientation"]
    }
