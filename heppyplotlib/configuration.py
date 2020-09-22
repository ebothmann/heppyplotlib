"""Configure heppyplotlib or the underlying matplotlib."""

import matplotlib.pyplot as plt

def use_tex(use_serif=True, overwrite=True, preamble=None):
    """Configure pyplot to use LaTeX for text rendering."""

    if plt.rcParams['text.usetex'] and not overwrite:
        print("Will not override tex settings ...")
        return

    print("Will use tex for rendering ...")

    if preamble is None:
        if use_serif:
            plt.rc('font', family='serif')
            preamble = [r'\usepackage{amsmath}',
                        r'\usepackage{siunitx}',
                        r'\usepackage{hepnames}']
        else:
            # note that we do note even have a capital delta character (\Delta) apparently ...
            # TODO: use a more complete sans serif font
            preamble = [r'\usepackage{amsmath}',
                        r'\renewcommand*\familydefault{\sfdefault}',
                        r'\usepackage{siunitx}',
                        r'\usepackage{hepnames}',
                        r'\sisetup{number-mode=text}',  # force siunitx to actually use your fonts
                        r'\usepackage{sansmath}',       # load up the sansmath for sans-serif math
                        r'\sansmath']                   # enable sansmath
    plt.rcParams['text.latex.preamble'] = preamble
    plt.rc('text', usetex=True)


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
              'figure.titlesize': normal,
              'axes.titlesize': normal,
              'axes.labelsize': normal,
              'legend.fontsize': small,
              'xtick.labelsize': small,   # \thefontsize\footnotesize (like subcaptions)
              'ytick.labelsize': small}
    plt.rcParams.update(params)


def set_figure_size(latex_width, aspect_ratio=0.6875):
    r"""Set figure size given a width in LaTeX points.

    Match LaTeX paper text width using:

    .. code-block:: latex

        \the\textwidth

    """
    tex_points_per_inch = 72.27
    inches_per_tex_point = 1.0 / tex_points_per_inch
    inches_width = latex_width * inches_per_tex_point
    plt.rc('figure', figsize=[inches_width, inches_width * aspect_ratio])
