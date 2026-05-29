def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms 'slices' into the decision variables used in the reference model.

    Args:
        ovar_dict (dict): Output from solver with key "slices" (list of [r1,c1,r2,c2]).
        n (int): number of rows of the pizza
        m (int): number of columns of the pizza
        patterns (List[Tuple[int,int]]): list of valid slice shapes (height,width)

    Returns:
        dict: {"x": ..., "s": ..., "z": ...}
    """
    slices = ovar_dict["slices"]
    maxSize = param_dict['maxSize']
    minIngredients = param_dict['minIngredients']
    pizza = param_dict['pizza']
    n, m = len(pizza), len(pizza[0])  # nRows and nColumns

    patterns = [(i, j) for i in range(1, min(maxSize, n) + 1) for j in range(1, min(maxSize, m) + 1) if 2 * minIngredients <= i * j <= maxSize]


    nPatterns = len(patterns)
    x = [[[0 for _ in range(nPatterns)] for _ in range(m)] for _ in range(n)]
    # s = [[[0 for _ in range(nPatterns)] for _ in range(m)] for _ in range(n)]

    # total_area = 0

    for (r1, c1, r2, c2) in slices:
        height = r2 - r1 + 1
        width = c2 - c1 + 1
        # area = height * width
        if (height, width) not in patterns:
            raise ValueError(f"Slice {(r1,c1,r2,c2)} not in valid patterns")

        k = patterns.index((height, width))
        x[r1][c1][k] = 1
        # s[r1][c1][k] = area
        # total_area += area

    return {
        "x": x,
        # "s": s,
        "z": ovar_dict["total_cells"]
    }
