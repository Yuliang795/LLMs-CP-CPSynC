def ovar_transformer(ovar_dict, param_dict):
    """
    For the SONET ring assignment problem, map 'objective' to 'z' and keep 'rings'.

    Args:
        ovar_dict: dict with 'objective': int, 'rings': List[List[int]]
        param_dict: dict (not used)

    Returns:
        dict: {'z': int, 'rings': List[List[int]]}
    """
    return {
        "z": ovar_dict["objective"],
        "rings": ovar_dict["rings"]
    }
