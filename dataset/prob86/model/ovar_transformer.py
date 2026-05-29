def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps generated output to the reference model variables.

    Args:
        ovar_dict (dict): expects
            - "schedule": List[int]
            - optionally "total_cost": int

    Returns:
        dict: keys matching reference model decision variables.
              Always returns {"x": schedule}. If "total_cost" is provided,
              also returns {"z": total_cost} for optional objective checking
              (if you introduce an auxiliary z in the model).
    """
    result = {"x": ovar_dict["schedule"]}
    result["z"] = ovar_dict["total_cost"]
    return result
