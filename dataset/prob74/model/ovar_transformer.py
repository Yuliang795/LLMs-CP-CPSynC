def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms requested output format:

        placements[k] = [[r1, c1], [r2, c2]]

    into reference model variables:

        x[i][j] = flattened position of the cell containing value i
        y[i][j] = flattened position of the cell containing value j

    Domino order:
        0-0, 0-1, ..., 0-6,
        1-1, 1-2, ..., 1-6,
        ...
        6-6
    """

    placements = ovar_dict["placements"]
    grid = param_dict["grid"]

    nRows = len(grid)
    nCols = len(grid[0])
    nValues = len(grid)

    x = [[None for _ in range(nValues)] for _ in range(nValues)]
    y = [[None for _ in range(nValues)] for _ in range(nValues)]

    dominoes = [(i, j) for i in range(nValues) for j in range(i, nValues)]

    if len(placements) != len(dominoes):
        raise ValueError(
            f"Expected {len(dominoes)} placements, but got {len(placements)}."
        )

    for idx, placement in enumerate(placements):
        i, j = dominoes[idx]

        if len(placement) != 2:
            raise ValueError(f"Domino {i}-{j} must have exactly two cells.")

        (r1, c1), (r2, c2) = placement

        pos1 = r1 * nCols + c1
        pos2 = r2 * nCols + c2

        val1 = grid[r1][c1]
        val2 = grid[r2][c2]

        if val1 == i and val2 == j:
            x[i][j] = pos1
            y[i][j] = pos2

        elif val1 == j and val2 == i:
            x[i][j] = pos2
            y[i][j] = pos1

        else:
            raise ValueError(
                f"Invalid placement for domino {i}-{j}: "
                f"cells ({r1}, {c1})={val1}, ({r2}, {c2})={val2}."
            )

    return {
        "x": x,
        "y": y,
    }