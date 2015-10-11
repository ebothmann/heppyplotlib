"""Functions for plotting data files."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def gridplot(file, uses_rivet_plot_info=True):
    """Convenience function to plot all YODA data objects from a YODA file into a subplots grid."""
    from . import yodaplot

    rivet_paths = yodaplot.data_object_names(file)

    # setup axes
    if len(rivet_paths) == 1:
        fig, ax = plt.subplots()
    else:
        ncols = 2
        nrows = (len(rivet_paths) - 1) / ncols + 1
        fig, ax = plt.subplots(nrows, ncols, squeeze=False)

    # plot into axes
    for rivet_path, axes in zip(rivet_paths, np.ravel(ax)):
        plt.sca(axes)
        plot(file, rivet_path, uses_rivet_plot_info=uses_rivet_plot_info)

def ratioplot(files, rivet_path, normalized=0, uses_rivet_plot_info=True):
    """Convenience function to plot a given data object
    from various files into a nominal pane and a diff pane"""
    from . import yodaplot

    fig, ax = ratioplots()
    plt.sca(ax[0])
    for file in files:
        label = file.replace('_', r'\_')
        plot(file, rivet_path, uses_rivet_plot_info=False, label=label)

    if uses_rivet_plot_info:
        from . import rivetplot
        legend_location = rivetplot.legend_location(rivet_path)
    else:
        legend_location = 'best'
    plt.legend(loc=legend_location)

    plt.sca(ax[1])

    if isinstance(normalized, int):
        normalized = files[normalized]

    divide_by = yodaplot.load_data_object(normalized, rivet_path)
    print divide_by
    for file in files:
        data_object = yodaplot.load_data_object(file, rivet_path, divide_by=divide_by)
        yodaplot.plot_data_object(data_object, visible=True)

    if uses_rivet_plot_info:
        from . import rivetplot
        rivetplot.apply_plot_info(rivet_path, ax[0], ax[1])

    layout_main_and_diff_axis(ax[0], ax[1])

def plot(file, rivet_path, uses_rivet_plot_info=True, **kwargs):
    """Plot a YODA data object from a YODA file."""
    from . import yodaplot
    print "Plotting", rivet_path, "from", file, "..."
    if uses_rivet_plot_info:
        from . import rivetplot
        errors_enabled = rivetplot.errors_enabled(rivet_path)
    yodaplot.plot(file, rivet_path, **kwargs)
    if uses_rivet_plot_info:
        rivetplot.apply_plot_info(rivet_path)

def ratioplots():
    fig = plt.figure()
    ax = []
    gs = gridspec.GridSpec(2, 1, height_ratios=[2,1])
    ax.append(plt.subplot(gs[0]))
    ax.append(plt.subplot(gs[1], sharex=plt.subplot(gs[0])))
    return fig, ax

def layout_main_and_diff_axis(main, diff):
    plt.gcf().subplots_adjust(hspace=0.0)
    main.spines['bottom'].set_visible(False)
    plt.setp(main.get_xticklabels(), visible=False)
    main.set_xlabel('')
    diff.xaxis.tick_bottom()
