"""Functions for plotting data objects within YODA files."""

import matplotlib.pyplot as plt
import numpy as np
import yoda

def plot(filename_or_data_object, data_object_name,
         errors_enabled=True, rebin_count=1, visible=True,
         **kwargs):
    """Plots a data object, potentially from a YODA file."""
    data_object = resolve_data_object(filename_or_data_object, data_object_name,
                                      rebin_count=rebin_count)
    return plot_data_object(data_object, errors_enabled, visible, **kwargs)

def plot_data_object(data_object,
                     errors_enabled=True, visible=True,
                     **kwargs):
    """Plots a YODA data object."""
    plotfunctions = {yoda.Scatter2D: plot_scatter2d, yoda.Histo1D: plot_histo1d}
    for classinfo, plotfunction in plotfunctions.items():
        if isinstance(data_object, classinfo):
            return plotfunction(data_object, errors_enabled, visible, **kwargs)
    raise Exception('Unknown type of YODA data object: ', data_object)

def get_y_coords(yoda_data_object):
    """Return y coordinates for a YODA data object of an unknown type."""
    getter_functions = {yoda.Scatter2D: get_scatter2d_y_coords, yoda.Histo1D: get_histo1d_y_coords}
    for classinfo, getter_function in getter_functions.items():
        if isinstance(yoda_data_object, classinfo):
            return getter_function(yoda_data_object)

def plot_scatter2d(scatter, errors_enabled=True, visible=True, **kwargs):
    """Plots a YODA Scatter2D object."""
    x_coords = [point.x for point in scatter.points]
    y_coords = get_scatter2d_y_coords(scatter)
    if visible:
        x_errs = []
        x_errs.append([point.xErrs[0] for point in scatter.points])
        x_errs.append([point.xErrs[1] for point in scatter.points])
        bins_are_adjacent = are_points_with_errors_adjacent(x_coords, x_errs)
        if errors_enabled:
            y_errs = []
            y_errs.append([point.yErrs[0] for point in scatter.points])
            y_errs.append([point.yErrs[1] for point in scatter.points])
        else:
            y_errs = None
    else:
        bins_are_adjacent = False
        x_errs = None
        y_errs = None
    if not bins_are_adjacent:
        return plt.errorbar(x_coords, y_coords,
                            fmt='o', xerr=x_errs, yerr=y_errs, visible=visible, **kwargs)
    else:
        return step_with_errorbar_using_points(x_coords, x_errs, y_coords, y_errs,
                                               errors_enabled=errors_enabled, visible=visible, **kwargs)

def get_scatter2d_y_coords(scatter):
    """Return y coordinates for a Scatter2D object."""
    return [point.y for point in scatter.points]

def plot_histo1d(histo, errors_enabled=True, visible=True, **kwargs):
    """Plots a YODA Histo1D object."""
    return plot_histo1d_bins(histo.bins, errors_enabled, visible, **kwargs)

def plot_histo1d_bins(bins, errors_enabled=True, visible=True, **kwargs):
    """Plots YODA Histo 1D bins."""
    x_lefts = [histo_bin.xEdges[0] for histo_bin in bins]
    widths = [histo_bin.xEdges[1] - histo_bin.xEdges[0] for histo_bin in bins]
    bins_are_adjacent = are_bins_adjacent(x_lefts, widths)
    y_coord = get_histo1d_y_coords(bins)
    y_errs = [histo_bin.heightErr for histo_bin in bins]
    if not bins_are_adjacent:
        result = plt.bar(x_lefts, y_coord, width=widths, yerr=y_errs, visible=visible, **kwargs)
    else:
        result = plot_step_with_errorbar(x_lefts, widths, y_coord, y_errs,
                                         errors_enabled=errors_enabled, visible=visible, **kwargs)
    # fix stupid automatic limits
    margins = (0, 0)  # (width[0]/4.0, width[-1]/4.0)
    plt.xlim(x_lefts[0] - margins[0], x_lefts[-1] + margins[1])
    return result

def get_histo1d_y_coords(histo_or_bins):
    """Return y coordinates for a Histo1D object."""
    if isinstance(histo_or_bins, yoda.Histo1D):
        bins = histo_or_bins.bins
    else:
        bins = histo_or_bins
    return [histo_bin.height for histo_bin in bins]

def are_points_with_errors_adjacent(points, errs):
    """Returns whether a given set of points are adjacent when taking their errors into account."""
    for i in range(len(points) - 1):
        point = points[i]
        err_right = errs[0][i]
        next_point = points[i + 1]
        next_err_left = errs[1][i + 1]
        right_edge = point + err_right
        left_edge = next_point - next_err_left
        if abs(left_edge - right_edge) > (err_right + next_err_left) / 100.0:
            return False
    return True

def are_bins_adjacent(lefts, widths):
    """Returns whether a given set of bins are adjacent."""
    for left, width, next_left in zip(lefts[:-1], widths[:-1], lefts[1:]):
        if not left + width == next_left:
            return False
    return True

def step_with_errorbar_using_points(x_coords, x_errs, y_coords, y_errs,
                                    errors_enabled=True, **kwargs):
    """Makes a step plot with error bars from points."""
    left = [coord - err_left for coord, err_left in zip(x_coords, x_errs[0])]
    widths = [err_left + err_right for err_left, err_right in zip(x_errs[0], x_errs[1])]
    return plot_step_with_errorbar(left, widths, y_coords, y_errs, errors_enabled, **kwargs)

def plot_step_with_errorbar(lefts, widths, y_coords, y_errs,
                            errors_enabled=True, use_errorrects_for_legend=False, **kwargs):
    """Makes a step plot with error bars."""
    lefts.append(lefts[-1] + widths[-1])
    y_coords.append(y_coords[-1])
    # prevent that we have labels for the step and the errorbar,
    # otherwise we have two legend entries per data set
    step_kwargs = dict(kwargs)
    rect_kwargs = dict(kwargs)
    if errors_enabled and "label" in kwargs:
        if use_errorrects_for_legend:
            del step_kwargs["label"]
        else:
            del rect_kwargs["label"]
    # delete kw args that are not defined for plt.step
    try:
        del step_kwargs["hatch"]
    except KeyError:
        pass
    step_result = plt.step(lefts, y_coords, where='post', **step_kwargs)
    if errors_enabled:
        try:
            ecolor = rect_kwargs["color"]
            del rect_kwargs["color"]
        except KeyError:
            ecolor = plt.gca().lines[-1].get_color()  # do not use the next color from the color cycle
        zorder = plt.gca().lines[-1].get_zorder() - 1  # make sure it's drawn below
        errorrects_result = plot_errorrects(lefts, y_coords, y_errs, ecolor, zorder, **rect_kwargs)
        # x_mids = [left + width / 2.0 for left, width in zip(lefts[:-1], widths)]
        # plt.errorbar(x_mids, y_coords[:-1], fmt='none', yerr=y_errs, ecolor=ecolor)
    else:
        errorrects_result = None
    return step_result, errorrects_result

def plot_errorrects(lefts, y_coords, y_errs, color, zorder=1, **kwargs):
    """Draws the y errors as an envelope for a step plot."""
    try:
        if not len(y_errs) == len(lefts) - 1:
            y_errs = zip(*y_errs)  # try transposing
            if not len(y_errs) == len(lefts) - 1:
                raise Exception("There are less y errors than points.")
    except TypeError:
        pass
    lefts = np.ravel(zip(lefts[:-1], lefts[1:]))
    try:
        y_down = np.ravel([[y - y_err[0]] * 2 for y, y_err in zip(y_coords, y_errs)])
        y_up = np.ravel([[y + y_err[1]] * 2 for y, y_err in zip(y_coords, y_errs)])
    except TypeError:
        y_down = np.ravel([[y - y_err] * 2 for y, y_err in zip(y_coords, y_errs)])
        y_up = np.ravel([[y + y_err] * 2 for y, y_err in zip(y_coords, y_errs)])
    if 'hatch' in kwargs:
        return plt.fill_between(lefts, y_up, y_down,
                                color='none',
                                edgecolor=color,
                                zorder=zorder, **kwargs)
    else:
        if 'linewidth' in kwargs:
            del kwargs['linewidth']
        if not 'alpha' in kwargs:
            kwargs['alpha'] = 0.3
        return plt.fill_between(lefts, y_up, y_down,
                                color=color,
                                linewidth=0.0,
                                zorder=zorder, **kwargs)

def data_object_names(filename):
    """Retrieves all data object names from a YODA file."""
    data_objects = yoda.readYODA(filename)
    return [key for key in data_objects.keys()
            if not data_objects[key].type in ('Counter', 'Scatter1D')]

def resolve_data_object(filename_or_data_object, name, divide_by=None, rebin_count=1):
    """Take passed data object or loads a data object from a YODA file,
    and return it after dividing by divide_by."""
    if isinstance(filename_or_data_object, basestring):
        data_object = yoda.readYODA(filename_or_data_object)[name]
    else:
        data_object = filename_or_data_object.clone()
    if not rebin_count == 1:
        data_object.rebin(rebin_count)
    if divide_by is not None:
        divide_by = resolve_data_object(divide_by, name)
        if data_object.type == "Histo1D":
            data_object = data_object.divideBy(divide_by)
        elif data_object.type == "Scatter2D":
            # we make sure that also divide_by is a Scatter2D before using its points property
            for point, denominator_point in zip(data_object.points, yoda.mkScatter(divide_by).points):
                if denominator_point.y == 0.0:
                    new_y = 1.0
                    new_y_errs = [0.0, 0.0]
                else:
                    new_y = point.y / denominator_point.y
                    new_y_errs = [y_err / denominator_point.y for y_err in point.yErrs]
                # if new_y == 1.0 and point.yErrs == denominator_point.yErrs:
                #     # assume this is the same data set, so use the same relative error
                    # if denominator_point.y == 0.0:
                    #     new_y_errs = [0.0, 0.0]
                    # else:
                    #     new_y_errs = [y_err / denominator_point.y for y_err in denominator_point.yErrs]
                # else:
                #     # assume that we divide through an independent data set, use error propagation
                #     rel_y_errs = [(y_err / point.y + den_y_err / denominator_point.y)
                #                   for y_err, den_y_err in zip(point.yErrs, denominator_point.yErrs)]
                #     new_y_errs = [rel_y_err * new_y for rel_y_err in rel_y_errs]
                point.y = new_y
                point.yErrs = new_y_errs
    return data_object
