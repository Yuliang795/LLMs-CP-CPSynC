def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transform the social golfers schedule output into the reference model's variable format.

    Args:
        ovar_dict: dict with 'schedule': List[List[List[int]]]
        param_dict: dict (contains 'n_rounds', 'n_groups', 'n_per_group', 'n_golfers', etc.)

    Returns:
        dict: {'round_place_golfer': List[List[int]]}
              where each sublist is the flat assignment of golfers for each round
    """
    schedule = ovar_dict["schedule"]  # [n_rounds][n_groups][n_per_group]
    round_place_golfer = []

    for round_groups in schedule:
        # Flatten each round's groups into a single list of golfer IDs
        flat = []
        for group in round_groups:
            flat.extend(group)
        round_place_golfer.append(flat)

    return {
        "round_place_golfer": round_place_golfer
    }
