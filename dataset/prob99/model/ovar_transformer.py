def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transform the provided home/away schedule into the reference model vars.

    Input (always provided):
      ovar_dict = {
        "home": List[List[int]],   # shape [nWeeks][nPeriods]
        "away": List[List[int]],   # shape [nWeeks][nPeriods]
      }

    Returns:
      dict with keys for the reference model:
        - "x": List[List[int]]  # first team per match from home
        - "y": List[List[int]]  # second team per match from away
        - "m": List[List[int]]  # match numbers per (week,period) as per model's table
    """
    home = ovar_dict["home"]
    away = ovar_dict["away"]

    nTeams = param_dict["n"]
    nWeeks = nTeams - 1
    nPeriods = nTeams // 2
    nMatches = nTeams * (nTeams - 1) // 2

    def match_number(t1, t2):
        return nMatches - ((nTeams - t1) * (nTeams - t1 - 1)) // 2 + (t2 - t1 - 1)

    def unordered_match_number(a, b):
        t1, t2 = min(a, b), max(a, b)
        return match_number(t1, t2)

    m = [
        [unordered_match_number(home[w][p], away[w][p]) for p in range(nPeriods)]
        for w in range(nWeeks)
    ]

    return {"x": home, "y": away, "m": m}
