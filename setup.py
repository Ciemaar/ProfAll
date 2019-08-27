#!/usr/bin/env python

from setuptools import setup
import site
import os.path
site_packages_path = site.getsitepackages()[0]

setup(
    name='ProfAll',
    version='0.0.1',
    py_modules=['profall'],
    data_files=[(os.path.join(*site_packages_path.split(os.sep)[-3:]), ["profall.pth"])],
    url='',
    license='',
    author='Andy Fundinger',
    author_email='andy@fundinger.name',
    description='', install_requires=['influxdb'],
    zip_safe=False,
)
