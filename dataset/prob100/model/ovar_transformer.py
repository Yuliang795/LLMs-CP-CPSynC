def infer_d_from_c(c, demands):
    return [[demands[node] for node in row] for row in c]

def ovar_transformer(ovar_dict, param_dict=None):
    """
   
    """
    routes = ovar_dict["routes"]
    nNodes = param_dict["nNodes"]
    # sanity check: each route should start at depot 0
    # if any(r[0] != 0 for r in routes): raise ValueError("Each route must start with 0 (depot).")
    c_shifted = [row[1:nNodes] for row in routes]

    d = infer_d_from_c(c_shifted, param_dict["demands"])
    # print(ovar_dict)
    return {
        "c": c_shifted,
        "d": d,
        "z": ovar_dict["total_distance"],
    }
