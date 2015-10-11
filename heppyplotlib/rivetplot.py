"""Functions for plotting data objects within YODA files with Rivet plot info."""

from pprint import pprint

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator, NullLocator
import rivet

from . import configuration
from . import yodaplot



def errors_enabled(rivet_path):
    plot_info = load_plot_info(rivet_path)
    try:
        return bool(int(plot_info['ErrorBands']))
    except KeyError:
        return True

def legend_location(rivet_path):
    plot_info = load_plot_info(rivet_path)
    try:
        x = float(plot_info['LegendXPos'])
        y = float(plot_info['LegendXPos'])
        return (x, y)
    except KeyError:
        return 'best'

def apply_plot_info(rivet_path, main=None, diff=None):
    plot_info = load_plot_info(rivet_path)
    print "Rivet plot info:"
    pprint(plot_info)

    if main is None:
        main = plt.gca()
    upper = main

    if diff is None:
        lower = upper
    else:
        lower = diff

    # set labels and make sure we use tex if Rivet provides any labels
    requires_tex = False

    try:
        upper.set_title(plot_info['Title'])
        requires_tex = True
    except KeyError:
        pass

    string_setters = {'Title': upper.set_title, 'XLabel': lower.set_xlabel, 'YLabel': upper.set_ylabel}
    for key, setter in string_setters.items():
        try:
            setter(plot_info[key])
            requires_tex = True
        except KeyError:
            pass
    if requires_tex:
        configuration.use_tex()

    # set axis limits
    for setters, min_key, max_key in zip(((upper.set_xlim, lower.set_xlim), (plt.ylim, )), prepend_x_y('Min'), prepend_x_y('Max')):
        try:
            for setter in setters:
                setter(float(plot_info[min_key]), float(plot_info[max_key]))
        except KeyError:
            pass

    # set tick locators
    axis_lists = ((upper.get_xaxis, lower.get_xaxis), (upper.get_yaxis, ))    
    for axis_list, key in zip(axis_lists, prepend_x_y('MajorTickMarks')):
        try:
            locator = MultipleLocator(int(plot_info[key]))
            for axis in axis_list:
                axis.set_major_locator()
        except KeyError:
            pass
    for axis_list, key in zip(axis_lists, prepend_x_y('MinorTickMarks')):
        try:
            nticks = int(plot_info[key])
            if nticks == 0:
                locator = NullLocator()
            else:
                locator = MaxNLocator(nbins=nticks + 1)
            for axis in axis_list:
                axis.set_minor_locator(locator)
        except KeyError:
            pass

    # set axis scales (note that Rivet has different defaults for x/y scales)
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

    # set diff-specialized properties
    if diff:
        try:
            diff.set_ylim(float(plot_info['RatioPlotYMin']), float(plot_info['RatioPlotYMax']))
        except KeyError:
            pass


def load_plot_info(rivet_path):
    plot_parser = rivet.mkStdPlotParser()
    return plot_parser.getHeaders(rivet_path)

def prepend_x_y(key):
    return ('X' + key, 'Y' + key)
