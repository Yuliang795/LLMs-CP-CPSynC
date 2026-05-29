#
#  def ovar_transformer(ovar_dict, param_dict):
#     """
#     Pads the grid with two extra dead rows/columns on each side for reference model.

#     Args:
#         ovar_dict: dict with 'grid': List[List[int]] (size x size, borders 0)
#         param_dict: dict with 'size': int

#     Returns:
#         dict: {'grid': List[List[int]]} (size+4 x size+4)
#     """
#     grid = ovar_dict["grid"]  # shape [size][size]
#     size = param_dict["size"]

#     # Prepare a new grid of shape [size+4][size+4], all 0s
#     new_size = size + 4
#     augmented = [[0 for _ in range(new_size)] for _ in range(new_size)]

#     # Copy grid into the center
#     for i in range(size):
#         for j in range(size):
#             augmented[i+2][j+2] = grid[i][j]
#     return {"grid": augmented}


def ovar_transformer(ovar_dict, param_dict):
    """
    Pads the grid with two extra dead rows/columns on each side for the reference model,
    and computes z (the total number of alive cells in the central [2..size+1,2..size+1] area).

    Args:
        ovar_dict: dict with 'grid': List[List[int]] (size x size, borders 0)
        param_dict: dict with 'size': int

    Returns:
        dict: {'grid': List[List[int]], 'z': int}
    """
    grid = ovar_dict["grid"]  # shape [size][size]
    size = len(grid)
    
    # Compute z: sum of alive cells in the central region [2..size+1][2..size+1] (ignore the first and last two rows/columns)
    z = sum(
        grid[r][c]
        for r in range(2, size - 2)
        for c in range(2, size - 2)
    )

    print(f"Computed z: {z}")

    return {"grid": grid, "z": z}
