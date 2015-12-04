#! /usr/bin/env python2
"""Example for plotting a YODA histogram using heppyplotlib."""
import matplotlib.pyplot as plt
import heppyplotlib as hpl

# you can disable the usage of Rivet plot info
# also histogram errors might be omitted
hpl.plot("Analysis.yoda", "/ANALYSIS/OBSERVABLE",
         uses_rivet_plot_info=False,
         errors_enabled=False)

# hpl.plot calls plt.plot in the end, so you can use normal pyplot commands to customize
plt.xlabel(r'$p_T$')
plt.yscale('log')

plt.show()
plt.savefig('plot.pdf')
