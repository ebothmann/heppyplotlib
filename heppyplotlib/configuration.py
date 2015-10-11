"""Functions that configure heppyplotlib or the underlying matplotlib."""

import matplotlib.pyplot as plt

def use_tex():
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=[r'\usepackage{amsmath}'])
