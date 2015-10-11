"""Functions for plotting data files."""

import numpy as np
import matplotlib.pyplot as plt

def plot(file, rivet_paths='__all__', uses_rivet_plot_info=True):

    # conditionally import as we do not require Rivet/YODA to be installed
    from . import yodaplot
    if uses_rivet_plot_info:
        from . import rivetplot

    # normalize rivet_paths argument
    if isinstance(rivet_paths, str):
        if rivet_paths=='__all__':
            rivet_paths = yodaplot.data_object_names(file)
        else:
            rivet_paths = [rivet_paths]

    # setup axes
    if len(rivet_paths) == 1:
        fig, ax = plt.subplots()
    else:
        ncols = 2
        nrows = (len(rivet_paths) - 1) / ncols + 1
        fig, ax = plt.subplots(nrows, ncols, squeeze=False)

    # plot into axes
    for rivet_path, axes in zip(rivet_paths, np.ravel(ax)):
        print "Plotting", rivet_path, "from", file, " ..."
        plt.sca(axes)
        if uses_rivet_plot_info:
            rivetplot.plot(file, rivet_path)
        else:
            yodaplot.plot(file, rivet_path)
