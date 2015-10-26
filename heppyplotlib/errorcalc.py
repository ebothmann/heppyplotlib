"""Functions for calculating errors by combining different datasets."""

import math

def asymmetric_hessian_error(value_lists):
    """Calculate the asymmetric hessian error from a list of datasets,
    where the first dataset stems from a PDF CV run."""
    lows = []
    highs = []
    transposed_value_lists = zip(*value_lists)
    for values in transposed_value_lists:
        central_value = values[0]
        evs = values[1:]
        error = [0.0, 0.0]
        for i in range(0, len(evs), 2):
            (ev_p, ev_m) = evs[i:i+2]
            error[0] += max(ev_p - central_value, ev_m - central_value, 0)**2
            error[1] += max(central_value - ev_p, central_value - ev_m, 0)**2
        high = central_value + math.sqrt(error[0])
        low = central_value - math.sqrt(error[1])
        highs.append(high)
        lows.append(low)
    return (lows, highs)
