from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'heppyplotlib',

    # Versions should comply with PEP440
    version = '0.1.0.dev0',

    description = 'Plot histogrammed data with special support for HEP-related needs',
    long_description = long_description,

    url = 'https://github.com/ebothmann/heppyplotlib',

    author = 'Enrico Bothmann',
    author_email = 'enoix@web.de',

    license = 'MIT',

    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers for possible entries

        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    keywords='plot hep high energy physics cross section histogram bin binned data',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires = ['matplotlib', 'numpy', 'pyaml'],

    extras_require = {
            'Rivet':  ["rivet"],
            'YODA': ["yoda"],
        }
)
