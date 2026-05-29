def ovar_transformer(ovar_dict, param_dict=None):

    model_of_rack = ovar_dict["model_of_rack"]
    cards_in_rack = ovar_dict["cards_in_rack"]
    total_cost    = ovar_dict["total_cost"]

    # ! In the reference model, a dummy model [0,0,0] is appended at the END.
    # Its index is the original number of rack models.
    dummy_idx = param_dict["nModels"]
    #
    m = [dummy_idx if v == -1 else v for v in model_of_rack]

    return {"m": m, "nc": cards_in_rack, "z": total_cost}
