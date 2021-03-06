import re
from codecs import open
from glob import glob
from itertools import chain
from os import path

from setuptools import setup

from greendeploy import __version__

name = "greendeploy"
here = path.abspath(path.dirname(__file__))

# get package version
version = __version__

if not version:
    raise ValueError("Can't find the version in {name}/__init__.py")

setup(use_scm_version=True)
