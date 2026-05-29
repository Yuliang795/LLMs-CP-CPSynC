def ovar_transformer(ovar_dict, param_dict=None):
    """
    Map solution output to the reference model variables.

    Expected ovar_dict keys:
      - "killer": int in {0,1,2}
      - "hating": List[List[int]] shape [3][3], entries in {0,1}
      - "richer": List[List[int]] shape [3][3], entries in {0,1}

    Returns:
      dict with keys matching the reference model's decision variables:
        - "killer"
        - "hating"
        - "richer"
    """
    return {
        "killer": ovar_dict["killer"],
        "hating": ovar_dict["hating"],
        "richer": ovar_dict["richer"],
    }
