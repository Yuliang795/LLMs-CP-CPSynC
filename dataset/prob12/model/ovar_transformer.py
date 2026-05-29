def ovar_transformer(ovar_dict, param_dict):
    """
    Transforms the output for the bucket problem to match the reference model's x (with padding).

    Args:
        ovar_dict: dict with 'cost': int, 'sequence_of_states': List[int]
        param_dict: dict with 'input_max': int

    Returns:
        dict: {'cost': int, 'x': List[int] of length input_max}
    """
    cost = ovar_dict["cost"]
    seq = ovar_dict["sequence_of_states"]
    input_max = param_dict["input_max"]

    if len(seq) < input_max:
        pad_len = input_max - len(seq) + 1
        seq_padded = seq[1:] + [seq[-1]] * pad_len
    else:
        seq_padded = seq[:input_max]

    return {
        ## the inital state in the ref model has an cost, so set to cost+1
        "cost": cost+1,
        "x": seq_padded
    }
