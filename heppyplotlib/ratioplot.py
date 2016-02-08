"""Plot a main pane with the nominal distribution and a lower pane with the
ratio."""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator

from .plot import plot


def ratioplot(files_or_data_objects, rivet_path,
              divide_by=0, uses_rivet_plot_info=True,
              errors_enabled=None,
              axes_list=None, draws_legend=True,
              labels=None,
              **kwargs):
    """Convenience function to plot data objects (directly passed or taken from
    files) into a nominal pane and a diff pane"""

    # we do not want to iterate characters, so wrap a passed string in a list
    if isinstance(files_or_data_objects, basestring):
        files_or_data_objects = [files_or_data_objects]

    if axes_list is None:
        axes_list = ratioplots()[1]

    plt.sca(axes_list[0])
    plot_nominal(files_or_data_objects, rivet_path,
                 labels=labels, errors_enabled=errors_enabled, **kwargs)

    if draws_legend:
        if uses_rivet_plot_info:
            from . import rivetplot
            legend_loc_kwargs = rivetplot.legend_location_kwargs(rivet_path)
        else:
            legend_loc_kwargs = {'loc': 'best'}
        plt.legend(**legend_loc_kwargs)

    plt.sca(axes_list[1])

    if isinstance(divide_by, int):
        divide_by = files_or_data_objects[divide_by]

    plot_diff(files_or_data_objects, rivet_path, divide_by,
              errors_enabled=errors_enabled, **kwargs)

    if uses_rivet_plot_info:
        from . import rivetplot
        rivetplot.apply_plot_info(rivet_path, axes_list[0], axes_list[1])

    layout_main_and_diff_axis(axes_list[0], axes_list[1])

    return axes_list


def ratioplots():
    """Returns a figure and two axes on it intended for main and diff plots."""
    fig = plt.figure()
    axes_list = []
    grid = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    axes_list.append(plt.subplot(grid[0]))
    axes_list.append(plt.subplot(grid[1], sharex=plt.subplot(grid[0])))
    return fig, axes_list


def layout_main_and_diff_axis(main, diff):
    """Improves layout of a main-and-diff-plot figure by making them
    adjacent."""
    plt.gcf().subplots_adjust(hspace=0.0)
    main.spines['bottom'].set_visible(False)
    plt.setp(main.get_xticklabels(), visible=False)
    main.set_xlabel('')
    diff.xaxis.tick_bottom()
    subplot_max_ticks = len(diff.get_yticklabels())
    diff.yaxis.set_major_locator(MaxNLocator(nbins=subplot_max_ticks-1,
                                             prune='upper'))


def plot_nominal(files_or_data_objects, rivet_path, errors_enabled=None, labels=None, **kwargs):
    """Populate the upper (nominal) pane of a ratio plot."""
    for i, filename_or_data_object in enumerate(files_or_data_objects):
        if labels is not None:
            label = labels[i]
        else:
            try:
                label = filename_or_data_object.replace('_', r'\_')
            except AttributeError:
                label = filename_or_data_object.path.replace('_', r'\_')
        plot(filename_or_data_object, rivet_path,
             uses_rivet_plot_info=False,
             errors_enabled=errors_enabled,
             label=label,
             **kwargs)


def plot_diff(files_or_data_objects, rivet_path, divide_by, errors_enabled=None, **kwargs):
    "Populate the lower (diff) pane of a ratio plot."""
    from . import yodaplot
    for filename_or_data_object in files_or_data_objects:
        data_object = yodaplot.resolve_data_object(filename_or_data_object,
                                                   rivet_path,
                                                   divide_by=divide_by)
        plot(data_object, rivet_path,
             uses_rivet_plot_info=False,
             errors_enabled=errors_enabled,
             **kwargs)
