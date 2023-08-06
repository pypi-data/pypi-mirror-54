#!/usr/bin/env python
# import os
# import sys
# import re
# from os.path import abspath, dirname, join
from setuptools import setup, find_packages
# from macpath import curdir
# curPath = os.path.abspath(os.path.dirname(__file__))
# parentPath = os.path.split(curPath)[0]
# rootPath = os.path.split(parentPath)[0]
# sys.path.append(rootPath)

#CURDIR = dirname(abspath(__file__))
#print(CURDIR)
# with open(join(CURDIR, 'requirements.txt')) as f:
#     REQUIREMENTS = f.read().splitlines()
setup(
    name             = 'lgplibdemo',
    version          = '0.0.3',
    description      = 'library for Robot Framework',
    long_description = 'library for Robot Framework',
    author           = 'ligaopan',
    author_email     = 'ligaopan1984@163.com',
    url              = 'https://github.com/ligaopan/lgp-library',
    license          = 'MIT Licence',
    keywords         = 'robotframework testing testautomation',
    platforms        = 'any',
    python_requires  = '>=3.7.*',
    install_requires = [],
    package_dir      = {'': 'src'},
    packages         = find_packages('src')
    )