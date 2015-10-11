"""Functions for plotting data files."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def gridplot(filename, uses_rivet_plot_info=True):
    """Convenience function to plot all YODA data objects from a YODA file into a subplots grid."""
    from . import yodaplot

    rivet_paths = yodaplot.data_object_names(filename)

    # setup axes
    if len(rivet_paths) == 1:
        axes_list = plt.subplots()[1]
    else:
        ncols = 2
        nrows = (len(rivet_paths) - 1) / ncols + 1
        axes_list = plt.subplots(nrows, ncols, squeeze=False)[1]

    # plot into axes
    for rivet_path, axes in zip(rivet_paths, np.ravel(axes_list)):
        plt.sca(axes)
        plot(filename, rivet_path, uses_rivet_plot_info=uses_rivet_plot_info)

def ratioplot(files, rivet_path, normalized=0, uses_rivet_plot_info=True):
    """Convenience function to plot a given data object
    from various files into a nominal pane and a diff pane"""
    from . import yodaplot

    axes_list = ratioplots()[1]
    plt.sca(axes_list[0])
    for filename in files:
        label = filename.replace('_', r'\_')
        plot(filename, rivet_path, uses_rivet_plot_info=False, label=label)

    if uses_rivet_plot_info:
        from . import rivetplot
        legend_location_kwargs = rivetplot.legend_location_kwargs(rivet_path)
    else:
        legend_location_kwargs = {'loc': 'best'}
    plt.legend(**legend_location_kwargs)

    plt.sca(axes_list[1])

    if isinstance(normalized, int):
        normalized = files[normalized]

    divide_by = yodaplot.load_data_object(normalized, rivet_path)
    print divide_by
    for filename in files:
        data_object = yodaplot.load_data_object(filename, rivet_path, divide_by=divide_by)
        yodaplot.plot_data_object(data_object, visible=True)

    if uses_rivet_plot_info:
        from . import rivetplot
        rivetplot.apply_plot_info(rivet_path, axes_list[0], axes_list[1])

    layout_main_and_diff_axis(axes_list[0], axes_list[1])

def plot(filename, rivet_path, uses_rivet_plot_info=True, **kwargs):
    """Plot a YODA data object from a YODA file."""
    from . import yodaplot
    print "Plotting", rivet_path, "from", filename, "..."
    if uses_rivet_plot_info:
        from . import rivetplot
        errors_enabled = rivetplot.errors_enabled(rivet_path)
    else:
        errors_enabled = True
    yodaplot.plot(filename, rivet_path, errors_enabled=errors_enabled, **kwargs)
    if uses_rivet_plot_info:
        rivetplot.apply_plot_info(rivet_path)

def ratioplots():
    """Returns a figure and two axes on it intended for main and diff plots."""
    fig = plt.figure()
    axes_list = []
    grid = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    axes_list.append(plt.subplot(grid[0]))
    axes_list.append(plt.subplot(grid[1], sharex=plt.subplot(grid[0])))
    return fig, axes_list

def layout_main_and_diff_axis(main, diff):
    """Improves layout of a main-and-diff-plot figure by making them adjacent."""
    plt.gcf().subplots_adjust(hspace=0.0)
    main.spines['bottom'].set_visible(False)
    plt.setp(main.get_xticklabels(), visible=False)
    main.set_xlabel('')
    diff.xaxis.tick_bottom()
