"""Functions for calculating errors by combining different datasets."""

import math

def combine(files, rivet_path, error_calc):
    """Combine files[1]/rivet_path, files[2]/rivet_path, ...
    using an error_calc function from the heppyplotlib.error_calc
    module and return a YODA data object.

    files[0] is supposed to be the CV data set.
    """
    import yoda
    from . import yodaplot
    y_coord_list = []
    for file_name in files:
        data_object = yodaplot.load_data_object(file_name, rivet_path)
        y_coord_list.append(yodaplot.get_y_coords(data_object))
    errs = error_calc(y_coord_list)
    # make sure we are dealing with a scatter object to have the correct notion of errors
    scatter = yoda.mkScatter(data_object)
    for point, point_errs in zip(scatter.points, zip(*errs)):
        point.yErrs = point_errs
    return scatter

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
