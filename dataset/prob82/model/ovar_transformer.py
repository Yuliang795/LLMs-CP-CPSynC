def ovar_transformer(ovar_dict, param_dict=None):
    """
    Convert a solution in `matching` array format into the decision variable x
    used in the reference model.
    
    Parameters:
        matching (list[int]): A list where matching[i] is the partner of agent i.
        preferences (list[list[int]]): preferences[i] is the ordered list of other agents for agent i.
                                        Agents are 0-indexed.
    
    Returns:
        list[int]: The x array where x[i] is the index in preferences[i] of agent i's partner.
    """
    matching = ovar_dict['matching']
    preferences = param_dict['preferences']
    n = len(matching)
    x = [None] * n
    for i in range(n):
        partner = matching[i]
        # find the index of partner in preferences[i]
        k = preferences[i].index(partner)
        x[i] = k
    return {"x": x}
