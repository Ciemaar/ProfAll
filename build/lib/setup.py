#!/usr/bin/env python

from setuptools import setup
from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

setup(
    name='ProfAll',
    version='0.0.1',
    py_modules=['profall','site_info','setup'],
    package_data={'': ["profall.pth"]},
    data_files=[(site_packages_path, ["profall.pth"])],
    #packages=[''],
    url='',
    license='',
    author='Andy Fundinger',
    author_email='andy@fundinger.name',
    description='', install_requires=['influxdb']
)
