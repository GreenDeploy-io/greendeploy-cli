import re
from codecs import open
from glob import glob
from itertools import chain
from os import path

from setuptools import find_packages, setup

name = "greendeploy"
here = path.abspath(path.dirname(__file__))

# get package version
with open(path.join(here, name, "__init__.py"), encoding="utf-8") as f:
    result = re.search(r'__version__ = ["\']([^"\']+)', f.read())

    if not result:
        raise ValueError("Can't find the version in greendeploy/__init__.py")

    version = result.group(1)

setup(use_scm_version=True)
