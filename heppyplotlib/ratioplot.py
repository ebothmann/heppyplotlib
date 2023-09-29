"""Plot a main pane with the nominal distribution and a lower pane with the
ratio."""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator

from .plot import plot


def ratioplot(files_or_data_objects, rivet_path,
              divide_by=0,
              assume_correlated=False,
              uses_rivet_plot_info=True,
              errors_enabled=None,
              axes_list=None,
              draws_legend=True,
              legend_fraction_of_figure=None,
              labels=None,
              styles=None,
              diff_ylabel=None,
              n_ratio_plots=1,
              n_columns=1,
              nominal_height_ratio=None,
              squeeze=True,
              **kwargs):
    """Convenience function to plot data objects (directly passed or taken from
    files) into a nominal pane and a diff pane"""

    # we do not want to iterate characters, so wrap a passed string in a list
    if isinstance(files_or_data_objects, str):
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
        wspace = None if n_columns == 1 else 0.4
        grid = gridspec.GridSpec(1 + n_ratio_plots, n_columns,
                height_ratios=height_ratios, right=right, hspace=0, wspace=wspace)
        axes_column_list = ratioplot_setup_axes(grid)
    else:
        grid = None

    for i, axes_list in enumerate(axes_column_list):

        if axes_list[0] is not None:
            plt.sca(axes_list[0])
            plot_nominal(files_or_data_objects, rivet_path,
                         labels=labels, styles=styles,
                         errors_enabled=errors_enabled, **kwargs)

            if draws_legend and len(files_or_data_objects) > 1:
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
            if not assume_correlated:
                assume_correlated = divide_by
            divide_by = files_or_data_objects[divide_by]

        for diff in axes_list[1:]:
            if diff is not None:
                plt.sca(diff)

                plot_diff(files_or_data_objects, rivet_path, divide_by,
                          assume_correlated=assume_correlated,
                          styles=styles,
                          errors_enabled=errors_enabled,
                          **kwargs)

                if i == 0 and uses_rivet_plot_info:
                    from . import rivetplot
                    rivetplot.apply_plot_info(rivet_path, axes_list[0], diff)

                if i == 0 and diff_ylabel is not None:
                    plt.ylabel(diff_ylabel)

    if n_columns == 1 and squeeze:
        return axes_list, grid
    else:
        return axes_column_list, grid


def ratioplot_setup_axes(subplot_specs):
    """Returns a figure and two axes on it intended for main and diff plots."""
    axes_column_list = []
    nrows = subplot_specs.get_geometry()[0]
    ncols = subplot_specs.get_geometry()[1]
    for j in range(0, ncols):
        axes_list = []
        kwargs = {}
        if not j == 0:
            kwargs["sharey"] = axes_column_list[0][0]
        axes_list.append(plt.subplot(subplot_specs[j], **kwargs))
        for i in range(1, nrows):
            kwargs = {"sharex": plt.subplot(subplot_specs[0])}
            #if not j == 0:
            #    kwargs["sharey"] = axes_column_list[0][i]
            axes_list.append(plt.subplot(subplot_specs[i*ncols + j], **kwargs))
        layout_main_and_diff_axes(axes_list[0], axes_list[1:])
        axes_column_list.append(axes_list)
    return axes_column_list


def layout_axes_column(axes):
    """Improves layout of a axes columns that are adjacent."""
    for axis in axes[:-1]:
        axis.spines['bottom'].set_visible(False)
        plt.setp(axis.get_xticklabels(), visible=False)
        axis.set_xlabel('')
    axes[-1].xaxis.tick_bottom()
    for axis in axes[1:]:
        subplot_max_ticks = len(axes[-1].get_yticklabels())
        axis.yaxis.set_major_locator(MaxNLocator(nbins=subplot_max_ticks-1,
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


def plot_diff(files_or_data_objects, rivet_path, divide_by, assume_correlated="all", styles=None, errors_enabled=None, **kwargs):
    """Populate the lower (diff) pane of a ratio plot."""
    from . import yodaplot
    for i, filename_or_data_object in enumerate(files_or_data_objects):
        if isinstance(assume_correlated, int) and assume_correlated == i:
            assume_correlated_i = True
        elif isinstance(assume_correlated, str) and assume_correlated == "all":
            assume_correlated_i = True
        else:
            assume_correlated_i = assume_correlated
        data_object = yodaplot.resolve_data_object(filename_or_data_object,
                                                   rivet_path,
                                                   divide_by=divide_by,
                                                   assume_correlated=assume_correlated_i)
        local_kwargs = dict(kwargs)
        if styles is not None:
            local_kwargs.update(styles[i])
        plot(data_object, rivet_path,
             uses_rivet_plot_info=False,
             errors_enabled=errors_enabled,
             **local_kwargs)
