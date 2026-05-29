def ovar_transformer(ovar_dict, param_dict=None):
    """
    Map:
      - 'allergic' (by allergy index) -> foods VarArray [eggs, mold, nuts, ragweed]
      - 'surnames' (by surname index) -> surnames VarArray [baxter, lemon, malone, fleet]

    Friend indices: 0: Debra, 1: Janet, 2: Hugh, 3: Rick
    Allergy indices: 0: eggs, 1: mold, 2: nuts, 3: ragweed
    Surname indices: 0: Baxter, 1: Lemon, 2: Malone, 3: Fleet
    """
    friend_names = ["Debra", "Janet", "Hugh", "Rick"]

    allergic_idx = ovar_dict["allergic"]   # length 4, values in {0,1,2,3}
    surnames_idx = ovar_dict["surnames"]   # length 4, values in {0,1,2,3}

    foods = [friend_names[i] for i in allergic_idx]     # [eggs, mold, nuts, ragweed]
    surnames = [friend_names[i] for i in surnames_idx]  # [baxter, lemon, malone, fleet]

    return {"foods": foods, "surnames": surnames}
