#!/usr/bin/env python

"""
***********************************************************
***     THE HUMAN CELL ATLAS DCP CLI IS AVAILABLE AT    ***
***             https://pypi.org/project/hca/           ***
***                        OR VIA                       ***
***                  `pip install hca`                  ***
*** PLEASE REPLACE `hca-cli` WITH `hca` IN YOUR COMMAND ***
***********************************************************
"""

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class HCADevelopWarning(develop, install):
    def run(self):
        raise Exception(__doc__)


class HCAInstallWarning(install):
    def run(self):
        raise Exception(__doc__)


setup(
    name="hca-cli",
    version="0.1.2",
    url='https://pypi.org/project/hca',
    license='Apache Software License',
    author='Please see https://pypi.org/project/hca',
    author_email='akislyuk@chanzuckerberg.com',
    description='Please see https://pypi.org/project/hca',
    long_description='Please see https://pypi.org/project/hca',
    cmdclass={
        'develop': HCADevelopWarning,
        'install': HCAInstallWarning,
    }
)
