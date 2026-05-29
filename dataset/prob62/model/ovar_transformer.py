def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps generated output 'start_times' and 'makespan' to reference model variables 'x' and 'z'.
    Args:
        ovar_dict: dict with keys 'start_times', 'makespan'
    Returns:
        dict: with keys 'x', 'z'
    """
    return {
        "x": ovar_dict["start_times"],
        "z": ovar_dict["makespan"]
    }
