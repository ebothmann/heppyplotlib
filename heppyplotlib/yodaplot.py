"""Functions for plotting data objects within YODA files."""

import matplotlib.pyplot as plt
import numpy as np
import yoda

def plot(filename, data_object_name, errors_enabled=True, visible=True, **kwargs):
    """Plots a data object from a YODA file."""
    data_object = load_data_object(filename, data_object_name)
    plot_data_object(data_object, errors_enabled, visible, **kwargs)

def plot_data_object(data_object, errors_enabled=True, visible=True, **kwargs):
    """Plots a YODA data object."""
    plotfunctions = {yoda.Scatter2D: plot_scatter2d, yoda.Histo1D: plot_histo1d}
    for classinfo, plotfunction in plotfunctions.items():
        if isinstance(data_object, classinfo):
            plotfunction(data_object, errors_enabled, visible, **kwargs)
            return
    raise Exception('Unknown type of YODA data object: ', data_object)

def plot_scatter2d(scatter, errors_enabled=True, visible=True, **kwargs):
    """Plots a YODA Scatter2D object."""
    x_coords = [point.x for point in scatter.points]
    y_coords = [point.y for point in scatter.points]
    if errors_enabled and visible:
        x_errs = []
        x_errs.append([point.xErrs[0] for point in scatter.points])
        x_errs.append([point.xErrs[1] for point in scatter.points])
        y_errs = []
        y_errs.append([point.yErrs[0] for point in scatter.points])
        y_errs.append([point.yErrs[1] for point in scatter.points])
        bins_are_adjacent = are_points_with_errors_adjacent(x_coords, x_errs)
    else:
        bins_are_adjacent = False
        x_errs = None
        y_errs = None
    if not bins_are_adjacent:
        plt.errorbar(x_coords, y_coords,
                     fmt='o', xerr=x_errs, yerr=y_errs, visible=visible, **kwargs)
    else:
        step_with_errorbar_using_points(x_coords, x_errs, y_coords, y_errs,
                                        errors_enabled=errors_enabled, visible=visible, **kwargs)

def plot_histo1d(histo, errors_enabled=True, visible=True, **kwargs):
    """Plots a YODA Histo1D object."""
    x_lefts = [histo_bin.xEdges[0] for histo_bin in histo.bins]
    widths = [histo_bin.xEdges[1] - histo_bin.xEdges[0] for histo_bin in histo.bins]
    bins_are_adjacent = are_bins_adjacent(x_lefts, widths)
    y_coord = [histo_bin.height for histo_bin in histo.bins]
    y_errs = [histo_bin.heightErr for histo_bin in histo.bins]
    if not bins_are_adjacent:
        plt.bar(x_lefts, y_coord, width=widths, yerr=y_errs, visible=visible, **kwargs)
    else:
        plot_step_with_errorbar(x_lefts, widths, y_coord, y_errs,
                                errors_enabled=errors_enabled, visible=visible, **kwargs)
    # fix stupid automatic limits
    margins = (0, 0)  # (width[0]/4.0, width[-1]/4.0)
    plt.xlim(x_lefts[0] - margins[0], x_lefts[-1] + margins[1])

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
    plot_step_with_errorbar(left, widths, y_coords, y_errs, errors_enabled, **kwargs)

def plot_step_with_errorbar(lefts, widths, y_coords, y_errs,
                            errors_enabled=True, **kwargs):
    """Makes a step plot with error bars."""
    lefts.append(lefts[-1] + widths[-1])
    y_coords.append(y_coords[-1])
    plt.step(lefts, y_coords, where='post', **kwargs)
    if errors_enabled:
        ecolor = plt.gca().lines[-1].get_color()  # do not use the next color from the color cycle
        zorder = plt.gca().lines[-1].get_zorder() - 1  # make sure it's drawn below
        plot_errorrects(lefts, y_coords, y_errs, ecolor, zorder)
        # x_mids = [left + width / 2.0 for left, width in zip(lefts[:-1], widths)]
        # plt.errorbar(x_mids, y_coords[:-1], fmt='none', yerr=y_errs, ecolor=ecolor)

def plot_errorrects(lefts, y_coords, y_errs, color, zorder=1):
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
    plt.fill_between(lefts, y_up, y_down, color=color, alpha=0.3, zorder=zorder, linewidth=0)

def data_object_names(filename):
    """Retrieves all data object names from a YODA file."""
    data_objects = yoda.readYODA(filename)
    return data_objects.keys()

def load_data_object(filename, name, divide_by=None):
    """Loads a data object from a YODA file."""
    data_object = yoda.readYODA(filename)[name]
    if divide_by is not None:
        data_object = data_object.divideBy(divide_by)
    return data_object
