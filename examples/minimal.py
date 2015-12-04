#! /usr/bin/env python2
"""Minimal example for plotting a YODA histogram using heppyplotlib."""
import matplotlib.pyplot as plt
import heppyplotlib as hpl

hpl.plot("Analysis.yoda", "/ANALYSIS/OBSERVABLE")
plt.savefig('plot.pdf')
