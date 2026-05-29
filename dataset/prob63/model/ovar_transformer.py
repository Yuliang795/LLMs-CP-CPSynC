def to_internal_city(city, c):
    return c - 1 if city == 0 else city - 1


def trim_padded_tour(tour):
    # Keep everything through the first return to depot after the start.
    for i in range(1, len(tour)):
        if tour[i] == 0:
            return tour[:i + 1]
    return tour


def ovar_transformer(ovar_dict, param_dict=None):
    c = param_dict["c"]

    tour = trim_padded_tour(ovar_dict["tour"])
    p_locs = ovar_dict["p_locs"]

    # @@ mapping
    # spec uses depot 0
    # reference model uses depot c - 1
    tour = [to_internal_city(city, c) for city in tour]
    p_locs = [to_internal_city(city, c) for city in p_locs]

    x = list(range(c))
    for i in range(len(tour) - 1):
        x[tour[i]] = tour[i + 1]

    return {
        "x": x,
        "pl": p_locs,
        "z": ovar_dict["cost"]
    }