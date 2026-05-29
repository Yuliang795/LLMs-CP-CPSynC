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
    # check each letter is assigned
    # @@ hard coded params for this problem
    required_words = ["no", "no", "yes"]
    required_letters = set("".join(required_words))
    submitted_letters = set(k.lower() for k in assignment.keys())
    if submitted_letters != required_letters:
        raise ValueError(
            f"assignment must contain exactly the letters {sorted(required_letters)}, "
            f"but got {sorted(submitted_letters)}"
        )
    if len(submitted_letters) != len(set(submitted_letters)):
        raise ValueError("assignment contains duplicate letters after lowercasing")
    if any(not isinstance(d, int) for d in assignment.values()):
        raise ValueError("all assigned values must be integers")
    #
    x = [None] * 26
    for letter, digit in assignment.items():
        idx = ord(letter.lower()) - ord('a')
        x[idx] = digit
    return {"x": x}
