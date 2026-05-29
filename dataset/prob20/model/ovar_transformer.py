def ovar_transformer(ovar_dict, param_dict):
    """
    For the rehearsal scheduling problem, map 'order' to 'rehearsal_order' and pass 'total_waiting_time' as is.

    Args:
        ovar_dict: dict with 'order': List[int], 'total_waiting_time': int
        param_dict: dict (not used)

    Returns:
        dict: {'rehearsal_order': List[int], 'total_waiting_time': int}
    """
    return {
        "rehearsal_order": ovar_dict["order"],
        "total_waiting_time": ovar_dict["total_waiting_time"]
    }
