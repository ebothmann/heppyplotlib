"""Functions for calculating errors by combining different datasets."""

import math
import numpy as np

def combine(files, rivet_path, error_calc, rebin_count=None, rebin_counts=None):
    """Combine files[1]/rivet_path, files[2]/rivet_path, ...
    using an error_calc function from the heppyplotlib.error_calc
    module and return a YODA data object.

    files[0] is supposed to be the CV data set.
    """
    if rebin_count is not None and rebin_counts is not None:
        raise Exception("Only use one of the options 'rebin_count' and 'rebin_counts'.")
    elif rebin_count is not None:
        rebin_counts = [rebin_count] * len(files)
    elif rebin_counts is None:
        rebin_counts = [1] * len(files)
    import yoda
    from . import yodaplot
    y_coord_list = []
    for file_name, rebin_count in zip(files, rebin_counts):
        data_object = yodaplot.resolve_data_object(file_name, rivet_path, rebin_count=rebin_count)
        y_coord_list.append(yodaplot.get_y_coords(data_object))
    errs = error_calc(y_coord_list)
    # make sure we are dealing with a scatter object to have the correct notion of errors
    scatter = yoda.mkScatter(yodaplot.resolve_data_object(files[0],
        rivet_path, rebin_count=rebin_counts[0]))
    for point, point_errs in zip(scatter.points, zip(*errs)):
        point.yErrs = point_errs
    return scatter

def standard_error(value_lists):
    """Calculate the standard error from a list of datasets,
    where the first dataset stems from a CV run."""
    negative_errs = []
    positive_errs = []
    transposed_value_lists = zip(*value_lists)
    for values in transposed_value_lists:
        replicas = values[1:]
        central_value = np.mean(replicas)
        sum_of_squared_deviations = 0.0
        for replica in replicas:
            sum_of_squared_deviations += (replica - central_value)**2
        error = math.sqrt(sum_of_squared_deviations / (len(replicas) - 1))
        negative_errs.append(error)
        positive_errs.append(error)
    return (negative_errs, positive_errs)

def asymmetric_hessian_error(value_lists):
    """Calculate the asymmetric hessian error from a list of datasets,
    where the first dataset stems from a PDF CV run."""
    negative_errs = []
    positive_errs = []
    transposed_value_lists = zip(*value_lists)
    for values in transposed_value_lists:
        central_value = values[0]
        evs = values[1:]
        error = [0.0, 0.0]
        for i in range(0, len(evs), 2):
            (ev_p, ev_m) = evs[i:i+2]
            error[0] += max(central_value - ev_p, central_value - ev_m, 0)**2
            error[1] += max(ev_p - central_value, ev_m - central_value, 0)**2
        negative_errs.append(math.sqrt(error[0]))
        positive_errs.append(math.sqrt(error[1]))
    return (negative_errs, positive_errs)

def envelope_error(value_lists):
    """Calculate the envelope of a list of datasets.
    The returned "errors" are relative to the first dataset."""
    negative_errs = []
    positive_errs = []
    transposed_value_lists = zip(*value_lists)
    for values in transposed_value_lists:
        negative_errs.append(values[0] - min(values))
        positive_errs.append(max(values) - values[0])
    return (negative_errs, positive_errs)
