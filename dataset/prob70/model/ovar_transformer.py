# Reference model function to compute nBins
def n_bins(weights, capacity):
    cnt = 0
    curr_load = 0

    for weight in weights:
        if curr_load + weight > capacity:
            cnt += 1
            curr_load = weight
        else:
            curr_load += weight

    if curr_load > 0:
        cnt += 1

    return cnt


def max_items_per_bin(weights, capacity):
    curr = 0
    for i, weight in enumerate(weights):
        curr += weight
        if curr > capacity:
            return i

    # If all items can fit in one bin, then max items per bin is len(weights)
    return len(weights)


def ovar_transformer(ovar_dict, param_dict):
    """
    Maps 'bins' and 'num_bins' to reference model variables 'x' and 'z',
    consistent with the bin packing model.
    """
    weights = param_dict["itemWeights"]
    capacity = param_dict["binCapacity"]
    bins = ovar_dict["bins"]
    # ! sorted weights wrt ref model
    weights_sorted = sorted(weights)

    nBins = n_bins(weights_sorted, capacity)
    maxPerBin = max_items_per_bin(weights_sorted, capacity)

    # Map original item index to weight
    item_weights = weights

    # Build bin contents
    bin_contents = [[] for _ in range(nBins)]
    for item_idx, bin_idx in enumerate(bins):
        bin_contents[bin_idx].append(item_weights[item_idx])

    # Sort and pad bins
    x = []
    for b in bin_contents:
        sorted_bin = sorted(b, reverse=True)
        padded = sorted_bin + [0] * (maxPerBin - len(sorted_bin))
        x.append(padded)

    # Ensure total rows == nBins
    while len(x) < nBins:
        x.append([0] * maxPerBin)

    return {
        "x": x,
        "z": ovar_dict["num_bins"]
    }