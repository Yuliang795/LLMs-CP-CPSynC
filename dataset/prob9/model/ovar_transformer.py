
def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transform the Battleships output grid to the reference model's board encoding,
    with water filler cells for the 0 and (width+1)/(height+1) rows and columns.

    Args:
        ovar_dict: dict with 'grid': List[List[str]]
        param_dict: dict with 'width' and 'height' (optional, can infer from grid)

    Returns:
        dict: {'board': List[List[int]]}
    """
    code_map = {".": 1, "c": 2, "l": 3, "r": 4, "t": 5, "b": 6, "m": 7}
    grid = ovar_dict["grid"]
    # Infer width and height from grid if not in param_dict
    n_rows = len(grid)
    n_cols = len(grid[0]) if grid else 0

    # Build inner grid: map each character to int
    inner_board = [[code_map[cell] for cell in row] for row in grid]

    # Create water row (all 1s) for padding
    water_row = [1] * (n_cols + 2)

    # Build full board with water padding
    board = [water_row]  # Top padding row
    for row in inner_board:
        board.append([1] + row + [1])  # Left/right padding
    board.append(water_row)           # Bottom padding row

    return {"board_": board}