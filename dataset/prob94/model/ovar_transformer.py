def ovar_transformer(ovar_dict, param_dict=None):
    """
    Map the generated solution to the reference model variables.

    Expected in ovar_dict:
      - "digits": List[int] of length 9, the values for d1..d9

    Returns:
      {"x": [...]} to bind to the reference model's VarArray x
    """
    digits = ovar_dict["digits"]
    # if len(digits) != 9:
    #     raise ValueError("digits must have length 9")
    return {"x": digits}
