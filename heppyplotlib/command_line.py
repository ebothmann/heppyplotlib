import sys

import heppyplotlib as hpl

if not len(sys.argv) == 3:
    print("usage: {} analysis.yoda /ANALYSIS/HISTOGRAM".format(sys.argv[0]))
    sys.exit(1)

hpl.plot(sys.argv[1], sys.argv[2])
