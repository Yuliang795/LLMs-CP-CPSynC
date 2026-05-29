def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transform the solver's indexed outputs into the reference model's variables.

    Input (all required):
      ovar_dict = {
        "payment_family": [cash_family, credit_family, ham_family, peas_family],  # each in {0..3}
        "item_buyer":     [flour_family, kerosene_family, muslin_family, sugar_family]  # each in {0..3}
      }

    Returns (keys match reference model variable names):
      {
        "flour":   <str>,
        "kerosene":<str>,
        "cloth":   <str>,   # 'muslin' in the statement is 'cloth' in the model
        "sugar":   <str>,
        "cash":    <str>,
        "credit":  <str>,
        "ham":     <str>,
        "peas":    <str>,
      }
    """
    fam = ["Boyds", "Garveys", "Logans", "Navarros"]

    pf = ovar_dict["payment_family"]  # [cash, credit, ham, peas] as family indices
    ib = ovar_dict["item_buyer"]      # [flour, kerosene, muslin, sugar] as family indices

    payment_family = [fam[i] for i in pf]
    item_buyer = [fam[i] for i in ib]

    # return {
    #     # items
    #     "flour":   fam[ib[0]],
    #     "kerosene":fam[ib[1]],
    #     "cloth":   fam[ib[2]],  # muslin -> cloth
    #     "sugar":   fam[ib[3]],
    #     # payments
    #     "cash":    fam[pf[0]],
    #     "credit":  fam[pf[1]],
    #     "ham":     fam[pf[2]],
    #     "peas":    fam[pf[3]],
    # }
    return {"payment_family":payment_family, "item_buyer":item_buyer}
