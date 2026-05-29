def ovar_transformer(ovar_dict, param_dict=None):
    """
    OPD (⟨v,b,r⟩) — map generated output to the reference model variables.

    Input (always provided per spec):
      ovar_dict = {
        "matrix": List[List[int]],   # shape [v][b], entries in {0,1}
        "lambda_val": int            # max dot product over all distinct row pairs
      }

    Returns:
      dict with keys aligned to the reference model:
        - "x": the 0/1 matrix
        - "lam": the reported maximum dot product (aux var you’ll add below)
    """
    return {
        "x": ovar_dict["matrix"],
        "lambda_val": ovar_dict["lambda_val"]
    }
