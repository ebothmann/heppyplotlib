"""Functions for plotting data files."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator

def gridplot(file_name, uses_rivet_plot_info=True):
    """Convenience function to plot all :py:mod:`yoda` data objects
    from a :py:mod:`yoda` file into a subplots grid.

    :param str file_name: The path to the :py:mod:`yoda` file.
    :return: fig, axes_list
    """
    from . import yodaplot

    rivet_paths = yodaplot.data_object_names(file_name)

    # setup axes
    if len(rivet_paths) == 1:
        fig, axes_list = plt.subplots()
    else:
        ncols = 2
        nrows = (len(rivet_paths) - 1) / ncols + 1
        fig, axes_list = plt.subplots(nrows, ncols, squeeze=False)

    # plot into axes
    for rivet_path, axes in zip(rivet_paths, np.ravel(axes_list)):
        plt.sca(axes)
        plot(file_name, rivet_path, uses_rivet_plot_info=uses_rivet_plot_info)

    return fig, axes_list

def ratioplot(files_or_data_objects, rivet_path,
              divide_by=0, uses_rivet_plot_info=True, axes_list=None, draws_legend=True):
    """Convenience function to plot data objects (directly passed or taken from files)
    into a nominal pane and a diff pane"""
    import yoda
    from . import yodaplot

    if isinstance(files_or_data_objects, basestring):
        files_or_data_objects = [files_or_data_objects]

    if axes_list is None:
        axes_list = ratioplots()[1]

    plt.sca(axes_list[0])
    for filename_or_data_object in files_or_data_objects:
        try:
            label = filename_or_data_object.replace('_', r'\_')
        except AttributeError:
            label = filename_or_data_object.path.replace('_', r'\_')
        plot(filename_or_data_object, rivet_path, uses_rivet_plot_info=False, label=label)

    if draws_legend:
        if uses_rivet_plot_info:
            from . import rivetplot
            legend_location_kwargs = rivetplot.legend_location_kwargs(rivet_path)
        else:
            legend_location_kwargs = {'loc': 'best'}
        plt.legend(**legend_location_kwargs)

    plt.sca(axes_list[1])

    if isinstance(divide_by, int):
        divide_by = files_or_data_objects[divide_by]
    divide_by = yodaplot.resolve_data_object(divide_by, rivet_path)

    for filename_or_data_object in files_or_data_objects:
        data_object = yodaplot.resolve_data_object(filename_or_data_object, rivet_path,
                                                   divide_by=divide_by)
        yodaplot.plot_data_object(data_object, visible=True)

    if uses_rivet_plot_info:
        from . import rivetplot
        rivetplot.apply_plot_info(rivet_path, axes_list[0], axes_list[1])

    layout_main_and_diff_axis(axes_list[0], axes_list[1])

    return axes_list

def plot(filename, rivet_path, uses_rivet_plot_info=True, errors_enabled=None, **kwargs):
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

def plot_data_object(data_object, rivet_path,
                     uses_rivet_plot_info=True, errors_enabled=None, **kwargs):
    """Plot a YODA data object."""
    from . import yodaplot
    if uses_rivet_plot_info:
        from . import rivetplot
    if uses_rivet_plot_info and errors_enabled is None:
        errors_enabled = rivetplot.errors_enabled(rivet_path)
    yodaplot.plot_data_object(data_object, errors_enabled=errors_enabled, **kwargs)
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
    subplot_max_ticks = len(diff.get_yticklabels())
    diff.yaxis.set_major_locator(MaxNLocator(nbins=subplot_max_ticks-1, prune='upper'))
