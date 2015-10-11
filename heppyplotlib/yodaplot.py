"""Functions for plotting data objects within YODA files."""

import matplotlib.pyplot as plt
import yoda

def data_object_names(file):
    data_objects = yoda.readYODA(file)
    return data_objects.keys()

def plot(file, data_object_name, errors_enabled=True, visible=True, **kwargs):
    data_object = load_data_object(file, data_object_name)
    plot_data_object(data_object, errors_enabled, visible, **kwargs)

def plot_data_object(data_object, errors_enabled=True, visible=True, **kwargs):
    plotfunctions = {yoda.Scatter2D: plot_scatter2d, yoda.Histo1D: plot_histo1d}
    for classinfo, plotfunction in plotfunctions.items():
        if isinstance(data_object, classinfo):
            plotfunction(data_object, errors_enabled, visible, **kwargs)
            return
    raise Exception('Unknown type of YODA data object: ', data_object)

def load_data_object(file, name, divide_by=None):
    data_object = yoda.readYODA(file)[name]
    if divide_by is not None:
        data_object = data_object.divideBy(divide_by)
    return data_object

def plot_scatter2d(scatter, errors_enabled=True, visible=True, **kwargs):
    x = [point.x for point in scatter.points]
    y = [point.y for point in scatter.points]
    if errors_enabled and visible:
        x_errs = []
        x_errs.append([point.xErrs[0] for point in scatter.points])
        x_errs.append([point.xErrs[1] for point in scatter.points])
        y_errs = []
        y_errs.append([point.yErrs[0] for point in scatter.points])
        y_errs.append([point.yErrs[1] for point in scatter.points])
        bins_are_adjacent = True
        for current_x, current_x_err_right, next_x, next_x_err_left in zip(x[:-1], x_errs[0][:-1], x[1:], x_errs[1][1:]):
            right_edge = current_x + current_x_err_right
            left_edge = next_x - next_x_err_left
            if abs(left_edge - right_edge) > (current_x_err_right + next_x_err_left) / 100.0:
                bins_are_adjacent = False
                break
    else:
        bins_are_adjacent = False
        x_errs = None
        y_errs = None
    if not bins_are_adjacent:
        plt.errorbar(x, y, fmt='o', yerr=y_errs, xerr=x_errs, visible=visible, **kwargs)
    else:
        x_lefts = [current_x - current_x_err_left for current_x, current_x_err_left in zip(x, x_errs[0])]
        x_lefts.append(x_lefts[-1] + x_errs[1][-1])
        y.append(y[-1])
        plt.step(x_lefts, y, where='post', visible=visible, **kwargs)

def plot_histo1d(histo, errors_enabled=True, visible=True, **kwargs):
    x_lefts = [bin.xEdges[0] for bin in histo.bins]
    widths = [bin.xEdges[1] - bin.xEdges[0] for bin in histo.bins]
    bins_are_adjacent = True
    for x_left, width, next_x_left in zip(x_lefts[:-1], widths[:-1], x_lefts[1:]):
        if not x_left + width == next_x_left:
            bins_are_adjacent = False
            break
    y = [bin.height for bin in histo.bins]
    y_errs = [bin.heightErr for bin in histo.bins]
    if not bins_are_adjacent:
        plt.bar(x_lefts, y, width=widths, yerr=y_errs, visible=visible, **kwargs)
    else:
        x_lefts.append(x_lefts[-1] + widths[-1])
        y.append(y[-1])
        plt.step(x_lefts, y, where='post', visible=visible, **kwargs)
        if errors_enabled:
            x_mids = [left + width / 2.0 for left, width in zip(x_lefts[:-1], widths)]
            plt.gca().set_color_cycle(None)
            plt.errorbar(x_mids, y[:-1], fmt='none', yerr=y_errs, visible=visible)
    # fix stupid automatic limits
    margins = (0, 0)  # (width[0]/4.0, width[-1]/4.0)
    plt.xlim(x_lefts[0] - margins[0], x_lefts[-1] + margins[1])
