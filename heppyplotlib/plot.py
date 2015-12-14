"""Functions for plotting data files."""

import numpy as np
import matplotlib.pyplot as plt


def rivet_paths(file_name):
    """Return all :py:mod:`rivet` paths found at file_name."""
    from . import yodaplot
    return yodaplot.data_object_names(file_name)


def gridplot(file_name, uses_rivet_plot_info=True):
    """Convenience function to plot all :py:mod:`yoda` data objects
    from a :py:mod:`yoda` file into a subplots grid.

    :param str file_name: The path to the :py:mod:`yoda` file.
    :return: fig, axes_list
    """
    all_rivet_paths = rivet_paths(file_name)

    # setup axes
    if len(all_rivet_paths) == 1:
        fig, axes_list = plt.subplots()
    else:
        ncols = 2
        nrows = (len(all_rivet_paths) - 1) / ncols + 1
        fig, axes_list = plt.subplots(nrows, ncols, squeeze=False)

    # plot into axes
    for rivet_path, axes in zip(all_rivet_paths, np.ravel(axes_list)):
        plt.sca(axes)
        plot(file_name, rivet_path, uses_rivet_plot_info=uses_rivet_plot_info)

    return fig, axes_list


def plot(filename, rivet_path, uses_rivet_plot_info=True, errors_enabled=None,
         **kwargs):
    """Plot a YODA data object from a YODA file."""
    from . import yodaplot
    print "Plotting", rivet_path, "from", filename, "..."
    if uses_rivet_plot_info and errors_enabled is None:
        from . import rivetplot
        errors_enabled = rivetplot.errors_enabled(rivet_path)
    else:
        errors_enabled = True if errors_enabled is None else errors_enabled
    yodaplot.plot(filename, rivet_path, errors_enabled=errors_enabled,
                  **kwargs)
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
    yodaplot.plot_data_object(data_object, errors_enabled=errors_enabled,
                              **kwargs)
    if uses_rivet_plot_info:
        rivetplot.apply_plot_info(rivet_path)
