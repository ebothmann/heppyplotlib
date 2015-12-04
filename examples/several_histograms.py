#! /usr/bin/env python2
"""Example for plotting more than one YODA histogram using heppyplotlib."""
import matplotlib.pyplot as plt
import heppyplotlib as hpl

hpl.plot("Analysis.yoda", "/ANALYSIS/OBSERVABLE")
hpl.plot("Other_Analysis.yoda", "/OTHER/PATH")
plt.savefig('plot.pdf')

hpl.plot("Other_Analysis.yoda", "/SOME/PATH")
hpl.plot("Another_Analysis.yoda", "/ANOTHER/PATH")
hpl.plot("Yet_Another_Analysis.yoda", "/YET_ANOTHER/PATH")
plt.savefig('other_plot.pdf')
