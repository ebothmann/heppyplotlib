"""Plot a main pane with the nominal distribution and a lower pane with the
ratio."""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator

from .plot import plot


def ratioplot(files_or_data_objects, rivet_path,
              divide_by=0,
              use_correlated_division=True,
              uses_rivet_plot_info=True,
              errors_enabled=None,
              axes_list=None,
              draws_legend=True,
              legend_fraction_of_figure=None,
              labels=None,
              styles=None,
              diff_ylabel=None,
              n_ratio_plots=1,
              nominal_height_ratio=None,
              **kwargs):
    """Convenience function to plot data objects (directly passed or taken from
    files) into a nominal pane and a diff pane"""

    # we do not want to iterate characters, so wrap a passed string in a list
    if isinstance(files_or_data_objects, basestring):
        files_or_data_objects = [files_or_data_objects]

    if axes_list is None:
        plt.figure()
        if nominal_height_ratio is None:
            if n_ratio_plots > 2:
                nominal_height_ratio = 1
            else:
                nominal_height_ratio = 2
        height_ratios = [nominal_height_ratio] + [1]*n_ratio_plots
        right = None if legend_fraction_of_figure is None else 1-legend_fraction_of_figure
        grid = gridspec.GridSpec(1 + n_ratio_plots, 1, right=right, height_ratios=height_ratios, hspace=0)
        axes_list = ratioplot_setup_axes(grid)
    else:
        grid = None

    if axes_list[0] is not None:
        plt.sca(axes_list[0])
        plot_nominal(files_or_data_objects, rivet_path,
                     labels=labels, styles=styles,
                     errors_enabled=errors_enabled, **kwargs)

        if draws_legend:
            if legend_fraction_of_figure is None:
                if uses_rivet_plot_info:
                    from . import rivetplot
                    legend_loc_kwargs = rivetplot.legend_location_kwargs(rivet_path)
                else:
                    legend_loc_kwargs = {'loc': 'best'}
                plt.legend(**legend_loc_kwargs)
            else:
                handles, labels = axes_list[0].get_legend_handles_labels()
                plt.gcf().legend(handles, labels, loc="center right")

    if isinstance(divide_by, int):
        if not use_correlated_division:
            use_correlated_division = divide_by
        divide_by = files_or_data_objects[divide_by]

    for diff in axes_list[1:]:
        if diff is not None:
            plt.sca(diff)

            plot_diff(files_or_data_objects, rivet_path, divide_by,
                    use_correlated_division=use_correlated_division,
                    styles=styles,
                    errors_enabled=errors_enabled,
                    **kwargs)

            if uses_rivet_plot_info:
                from . import rivetplot
                rivetplot.apply_plot_info(rivet_path, axes_list[0], diff)

            if diff_ylabel is not None:
                plt.ylabel(diff_ylabel)

    return axes_list, grid


def ratioplot_setup_axes(subplot_specs):
    """Returns a figure and two axes on it intended for main and diff plots."""
    axes_list = []
    axes_list.append(plt.subplot(subplot_specs[0]))
    for i in range(1, subplot_specs.get_geometry()[0]):
        axes_list.append(plt.subplot(subplot_specs[i],
                                     sharex=plt.subplot(subplot_specs[0])))
    layout_main_and_diff_axes(axes_list[0], axes_list[1:])
    return axes_list


def layout_main_and_diff_axes(main, diffs):
    """Improves layout of a main-and-diffs-plot figure by making them
    adjacent."""
    for axis in [main] + diffs[:-1]:
        axis.spines['bottom'].set_visible(False)
        plt.setp(axis.get_xticklabels(), visible=False)
        axis.set_xlabel('')
    diffs[-1].xaxis.tick_bottom()
    for diff in diffs:
        subplot_max_ticks = len(diffs[-1].get_yticklabels())
        diffs[-1].yaxis.set_major_locator(MaxNLocator(nbins=subplot_max_ticks-1,
                                                      prune='upper'))


def plot_nominal(files_or_data_objects, rivet_path,
                 errors_enabled=None, styles=None,
                 labels=None, **kwargs):
    """Populate the upper (nominal) pane of a ratio plot."""
    for i, filename_or_data_object in enumerate(files_or_data_objects):
        if labels is not None:
            label = labels[i]
        else:
            try:
                label = filename_or_data_object.replace('_', r'\_')
            except AttributeError:
                label = filename_or_data_object.path.replace('_', r'\_')
        local_kwargs = dict(kwargs)
        if styles is not None:
            local_kwargs.update(styles[i])
        plot(filename_or_data_object, rivet_path,
             uses_rivet_plot_info=False,
             errors_enabled=errors_enabled,
             label=label,
             **local_kwargs)


def plot_diff(files_or_data_objects, rivet_path, divide_by, use_correlated_division="all", styles=None, errors_enabled=None, **kwargs):
    """Populate the lower (diff) pane of a ratio plot."""
    from . import yodaplot
    for i, filename_or_data_object in enumerate(files_or_data_objects):
        if isinstance(use_correlated_division, int) and use_correlated_division == i:
            use_correlated_division_i = True
        elif isinstance(use_correlated_division, str) and use_correlated_division == "all":
            use_correlated_division_i = True
        else:
            use_correlated_division_i = use_correlated_division
        data_object = yodaplot.resolve_data_object(filename_or_data_object,
                                                   rivet_path,
                                                   divide_by=divide_by,
                                                   use_correlated_division=use_correlated_division_i)
        local_kwargs = dict(kwargs)
        if styles is not None:
            local_kwargs.update(styles[i])
        plot(data_object, rivet_path,
             uses_rivet_plot_info=False,
             errors_enabled=errors_enabled,
             **local_kwargs)
