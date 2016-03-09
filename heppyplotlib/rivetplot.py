"""Functions for plotting data objects within YODA files with Rivet plot info."""

from pprint import pprint

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator, NullLocator
import rivet

from . import configuration

def errors_enabled(rivet_path):
    """Returns whether Rivet wants errors to be drawn."""
    plot_info = load_plot_info(rivet_path)
    try:
        return bool(int(plot_info['ErrorBands']))
    except KeyError:
        return True


def rebin_count(rivet_path):
    """Returns how many consecutive bins Rivet wants to be combined."""
    plot_info = load_plot_info(rivet_path)
    try:
        return int(plot_info['Rebin'])
    except KeyError:
        return 1


def legend_location_kwargs(rivet_path):
    """Returns what legend location Rivet wants us to use."""
    plot_info = load_plot_info(rivet_path)
    try:
        location_x = float(plot_info['LegendXPos'])
        location_y = float(plot_info['LegendYPos'])
        return {'bbox_to_anchor': (location_x, 1 - location_y), 'loc': 2}
    except KeyError:
        return {'loc': 'best'}

def apply_plot_info(rivet_path, main=None, diff=None):
    """Applies Rivet plot information to a main axes and optionally to a diff axes."""
    plot_info = load_plot_info(rivet_path)
    print "Rivet plot info:"
    pprint(plot_info)

    # normalize main argument
    if main is None:
        main = plt.gca()

    # map lower and upper axes, which are the same if there is no diff axes
    upper = main
    if diff is None:
        lower = upper
    else:
        lower = diff

    set_labels(plot_info, upper, lower)
    set_axis_limits(plot_info, upper, lower)
    set_tick_locators(plot_info, upper, lower)
    set_axis_scales(plot_info, upper, lower)

    # set diff-specialized properties
    if diff is not None:
        try:
            diff.set_ylim(float(plot_info['RatioPlotYMin']), float(plot_info['RatioPlotYMax']))
        except KeyError:
            pass

def set_labels(plot_info, upper, lower):
    """Sets labels from Rivet plot info."""
    requires_tex = False
    string_setters = {'Title': upper.set_title,
                      'XLabel': lower.set_xlabel, 'YLabel': upper.set_ylabel}
    for key, setter in string_setters.items():
        try:
            setter(plot_info[key])
            requires_tex = True
        except KeyError:
            pass
    if requires_tex:
        configuration.use_tex(overwrite=False)

def set_axis_limits(plot_info, upper, lower):
    """Sets axis limits from Rivet plot info."""
    setters_lists = ((upper.set_xlim, lower.set_xlim), (plt.ylim, ))
    for setters, min_key, max_key in zip(setters_lists, prepend_x_y('Min'), prepend_x_y('Max')):
        try:
            for setter in setters:
                setter(float(plot_info[min_key]), float(plot_info[max_key]))
        except KeyError:
            pass

def set_tick_locators(plot_info, upper, lower):
    """Sets major and minor tick locators from Rivet plot info."""
    axis_lists = ((upper.get_xaxis, lower.get_xaxis), (upper.get_yaxis, ))
    # NOTE: It's not clear to me how MajorTickMarks is supposed to work
    # for axis_list, key in zip(axis_lists, prepend_x_y('MajorTickMarks')):
    #     try:
    #         print int(plot_info[key])
    #         locator = MultipleLocator(int(plot_info[key]))
    #         for axis in axis_list:
    #             axis().set_major_locator(locator)
    #     except KeyError:
    #         pass
    for axis_list, key in zip(axis_lists, prepend_x_y('MinorTickMarks')):
        try:
            nticks = int(plot_info[key])
            if nticks == 0:
                locator = NullLocator()
            else:
                locator = MaxNLocator(nbins=nticks + 1)
            for axis in axis_list:
                axis().set_minor_locator(locator)
        except KeyError:
            pass

def set_axis_scales(plot_info, upper, lower):
    """Sets axis scales from Rivet plot info.
    Note that Rivet has different defaults for x and y scales."""
    try:
        logy = bool(int(plot_info['LogY']))
    except KeyError:
        logy = True
    if logy:
        upper.set_yscale('log')
    try:
        if int(plot_info['LogX']):
            upper.set_xscale('log')
            lower.set_xscale('log')
    except KeyError:
        pass

def load_plot_info(rivet_path):
    """Loads Rivet plot information."""
    plot_parser = rivet.mkStdPlotParser()
    return plot_parser.getHeaders(rivet_path)

def prepend_x_y(key):
    """Returns X... and Y... variants for a given string following a convention from Rivet."""
    return ('X' + key, 'Y' + key)
