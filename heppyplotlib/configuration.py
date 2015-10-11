"""Functions that configure heppyplotlib or the underlying matplotlib."""

import matplotlib.pyplot as plt

def use_tex():
    """Configures pyplot to use LaTeX for text rendering."""
    print "Will use tex for rendering ..."
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=[r'\usepackage{amsmath}',
                                   r'\renewcommand*\familydefault{\sfdefault}',
                                   r'\usepackage{sansmath}',
                                   r'\sansmath'])
