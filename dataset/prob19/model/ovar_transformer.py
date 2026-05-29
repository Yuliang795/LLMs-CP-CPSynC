def ovar_transformer(ovar_dict, param_dict):
    """
    For the warehouse location problem, map total_cost, supplier, cost directly, and convert open to bool list.

    Args:
        ovar_dict: dict with 'total_cost': int, 'supplier': List[int], 'cost': List[int], 'open': List[int]
        param_dict: dict (not used)

    Returns:
        dict: {'tot': int, 'supplier': List[int], 'cost': List[int], 'open': List[bool]}
    """
    supplier_list = ovar_dict["supplier"]
    # Adjust supplier indices to be 1-based 
    if min(supplier_list)==0:
        supplier_list = [x + 1 for x in supplier_list]  
    return {
        "tot": ovar_dict["total_cost"],
        "supplier": supplier_list,
        "cost": ovar_dict["cost"],
        "open": [bool(x) for x in ovar_dict["open"]]
    }
    # t1 = {'tot': 383, 'supplier': [5, 2, 5, 1, 5, 2, 2, 3, 2, 3], 'cost': [30, 27, 70, 2, 4, 22, 5, 13, 35, 55], 'open': [bool(x) for x in [1, 1, 1, 0, 1]]}
    # return t1
