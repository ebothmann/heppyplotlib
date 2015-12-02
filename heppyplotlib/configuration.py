"""Configure heppyplotlib or the underlying matplotlib."""

import matplotlib.pyplot as plt

def use_tex(useserif=False):
    """Configure pyplot to use LaTeX for text rendering."""
    print "Will use tex for rendering ..."
    plt.rc('text', usetex=True)
    if useserif:
        plt.rc('font', family='serif')
        preamble = [r'\usepackage{amsmath}',
                    r'\usepackage{siunitx}']
    else:
        preamble = [r'\usepackage{amsmath}',
                    r'\renewcommand*\familydefault{\sfdefault}',
                    r'\usepackage{siunitx}',
                    r'\sisetup{number-mode=text}',  # force siunitx to actually use your fonts
                    r'\usepackage{sansmath}',       # load up the sansmath for sans-serif math
                    r'\sansmath']                   # enable sansmath
    plt.rcParams['text.latex.preamble'] = preamble


def set_font_sizes(normal=9, small=8):
    r"""Configure pyplot to use these two font sizes.

    Match LaTeX paper font sizes using:

    .. code-block:: latex

        \makeatletter
        \newcommand\thefontsize[1]{{#1 The current font size is: \f@size pt\par}}
        \makeatother

    e.g. extract the font sizes for captions and subcaptions (as in the example)
    """
    params = {'font.size': normal,        # \thefontsize\small (like captions)
              'axes.labelsize': normal,
              'legend.fontsize': normal,
              'xtick.labelsize': small,   # \thefontsize\footnotesize (like subcaptions)
              'ytick.labelsize': small}
    plt.rcParams.update(params)


def set_figure_size(latex_width, aspect_ratio=0.6875):
    """Set figure size given a width in LaTeX points."""
    tex_points_per_inch = 72.27
    inches_per_tex_point = 1.0 / tex_points_per_inch
    inches_width = latex_width * inches_per_tex_point
    plt.rc('figure', figsize=[inches_width, inches_width * aspect_ratio])
