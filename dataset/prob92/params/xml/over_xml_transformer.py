def ovar_transformer(ovar_dict, param_dict=None):
    """
    Expect: ovar_dict = {"x": int}  # four-digit integer
    Return: {"x": x, "d": [d0,d1,d2,d3]} matching the reference model vars
    """
    x = ovar_dict["x"]
    # if not (1000 <= x <= 9999):
    #     raise ValueError("x must be a four-digit integer (1000..9999).")
    d = [x // 1000, (x // 100) % 10, (x // 10) % 10, x % 10]
    return {"x": x, "d": d}
