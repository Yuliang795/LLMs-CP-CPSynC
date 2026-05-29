def ovar_transformer(ovar_dict, param_dict=None):
    """
    Black Hole patience — map the output 'stack' into the reference model vars.

    Input (always provided):
      ovar_dict = {
        "stack": List[int]  # length nCards; stack[0] must be 0 (Ace of Spades)
      }

    Returns:
      {
        "x": List[int],  # same as stack: x[i] = card id at position i
        "y": List[int],  # inverse: y[card id] = position in stack
      }
    """
    stack = ovar_dict["stack"]
    nCards = len(stack)

    # x is exactly the play order
    x = stack[:]

    # y is the inverse permutation: position of each card id
    y = [0] * nCards
    for pos, card in enumerate(stack):
        y[card] = pos

    return {"x": x, "y": y}
