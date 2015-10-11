"""Functions for plotting data objects within YODA files with Rivet plot info."""

from pprint import pprint

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator, NullLocator
import rivet

from . import configuration
from . import yodaplot

string_setters = {'Title': plt.title, 'XLabel': plt.xlabel, 'YLabel': plt.ylabel}

def plot(file, rivet_path):
    plot_info = load_plot_info(rivet_path)
    print "Rivet plot info:"
    pprint(plot_info)

    # plot with or without error bands
    try:
        errors_enabled = bool(int(plot_info['ErrorBands']))
    except KeyError:
        errors_enabled = True
    yodaplot.plot(file, rivet_path, errors_enabled=errors_enabled)

    # set labels and make sure we use tex if Rivet provides any labels
    requires_tex = False
    for key, setter in string_setters.items():
        try:
            setter(plot_info[key])
            requires_tex = True
        except KeyError:
            pass
    if requires_tex:
        configuration.use_tex()

    # set axis limits
    for setter, min_key, max_key in zip((plt.xlim, plt.ylim), x_y_versions('Min'), x_y_versions('Max')):
        try:
            setter(float(plot_info[min_key]), float(plot_info[max_key]))
        except KeyError:
            pass

    # set tick locators
    axis_list = (plt.gca().xaxis, plt.gca().yaxis)    
    for axis, key in zip(axis_list, x_y_versions('MajorTickMarks')):
        try:
            axis.set_major_locator(MultipleLocator(int(plot_info[key])))
        except KeyError:
            pass
    for axis, key in zip(axis_list, x_y_versions('MinorTickMarks')):
        try:
            nticks = int(plot_info[key])
            if nticks == 0:
                locator = NullLocator()
            else:
                locator = MaxNLocator(nbins=nticks + 1)
            axis.set_minor_locator(locator)
        except KeyError:
            pass

    # set axis scales (note that Rivet has different defaults for x/y scales)
    try:
        logy = bool(int(plot_info['LogY']))            
    except KeyError:
        logy = True
    if logy:
        plt.yscale('log')
    try:
        if int(plot_info['LogX']):
            plt.xscale('log')
    except KeyError:
        pass

def load_plot_info(rivet_path):
    plot_parser = rivet.mkStdPlotParser()
    return plot_parser.getHeaders(rivet_path)

def x_y_versions(key):
    return ('X' + key, 'Y' + key)
