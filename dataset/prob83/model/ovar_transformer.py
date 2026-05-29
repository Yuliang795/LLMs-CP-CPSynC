def ovar_transformer(ovar_dict, param_dict=None):
    """
    Map 'women_matching' (hb) to the reference model's variables:
      - hb[w] = m (husband of woman w)
      - wf[m] = w (wife of man m)  [inverse of hb]

    Args:
        ovar_dict: dict with key 'women_matching' (List[int], length n)

    Returns:
        dict with keys:
          - 'hb': List[int] (size n)
          - 'wf': List[int] (size n)
    """
    hb = ovar_dict["women_matching"]          # hb[w] = man matched to woman w (0-based)
    n = len(hb)
    wf = [None] * n                           # wf[m] = woman matched to man m
    for w, m in enumerate(hb):
        wf[m] = w
    return {"hb": hb, "wf": wf}
