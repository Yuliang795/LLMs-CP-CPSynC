def ovar_transformer(ovar_dict, param_dict=None):
    """
    Maps the provided solution into the reference model variables.

    Expected keys in ovar_dict:
      - "culprit": int in {0,1,2}  (0=Alice, 1=Bob, 2=Sascha)
      - "liking":  List[List[int]] shape [3][3], entries in {0,1}
      - "taller":  List[List[int]] shape [3][3], entries in {0,1}

    Returns:
      dict with keys matching the reference model variables:
        - "culprit", "liking", "taller"
    """
    return {
        "culprit": ovar_dict["culprit"],
        "liking": ovar_dict["liking"],
        "taller": ovar_dict["taller"],
    }
