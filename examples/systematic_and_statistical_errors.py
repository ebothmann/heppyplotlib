#!/usr/bin/env python2
"""Example for plotting both systematic and statistical errors using
heppyplotlib."""
import heppyplotlib as hpl
import matplotlib.pyplot as plt

basenames = ["central", "up", "down"]
filepaths = [b + ".yoda" for b in basenames]

rivet_path = "/ANALYSIS/OBSERVABLE"

# plot systematic error as envelope over histograms
combined = hpl.combine(filepaths, rivet_path, hpl.envelope_error)
axes_list = hpl.ratioplot([combined], rivet_path,
                          use_errorrects_for_legend=True,
                          labels=[r"systematic"])[0]

# plot central histogram again with its statistical errors
hpl.ratioplot(filepaths[0], rivet_path,
              axes_list=axes_list,
              hatch=r"//",
              use_errorrects_for_legend=True,
              labels=["statistical"])

plt.savefig("plot.pdf")
