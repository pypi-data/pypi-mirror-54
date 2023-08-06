from setuptools import setup, find_packages
import re
import os

# Get package name from directory
name = "BayesianOptimization"

# Read version from __init__.py
with open('{}/__init__.py'.format(name), 'r') as file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        file.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(name             = name,
      version          = version,
      author           = 'Logan Grado',
      author_email     = 'grado.logan@gmail.com',
      description      = 'Bayesian Optimization',
      license          = '',
      url              = '',
      packages         = find_packages(),
      install_requires = ['numpy']
)
