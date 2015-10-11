# heppyplotlib
A package for plotting histogrammed data with special support for high energy physics applications.

## Installation

```
pip install git+https://github.com/ebothmann/heppyplotlib.git
```

## Usage

Plot a [YODA](yoda.hepforge.org) file generated using [Rivet](rivet.hepforge.org):

```python
import matplotlib.pyplot as plt
import heppyplotlib as hpl
hpl.plot('Analysis.yoda', '/ANALYSIS/HISTOGRAM')
plt.show()
```