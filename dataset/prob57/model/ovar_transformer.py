def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the generated 'order' list to the reference model's 'x' variable format (insertion position per cavity).
    Args:
        ovar_dict: dict, with keys 'order' (sequence of cavity indices) and 'cost'
    Returns:
        dict: with 'x' (list of positions per cavity) and 'z' (cost), ready for assignment in the reference model.
    """
    order = ovar_dict["order"]
    k = len(order)
    x = [order.index(i) for i in range(k)]
    result = {"x": x,
              "z": ovar_dict["cost"]}
    return result
