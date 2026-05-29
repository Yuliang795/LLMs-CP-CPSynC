def ovar_transformer(ovar_dict, param_dict=None):
    """
    Transforms the 'assignment' dict output to the reference model's 'x' array.
    Args:
        ovar_dict: dict, contains key 'assignment', mapping letters to digits.
    Returns:
        dict: with key 'x', value is a list of length 26: x[i] is the digit assigned to chr(ord('a')+i), or None if not assigned.
    """
    # ovar_dict = {'assignment': {'n': 5, 'o': 2, 'y': 1, 'e': 0, 's': 4}}
    assignment = ovar_dict["assignment"]
    x = [None] * 26
    for letter, digit in assignment.items():
        idx = ord(letter.lower()) - ord('a')
        x[idx] = digit
    return {"x": x}
