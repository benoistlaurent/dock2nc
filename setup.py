#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


# Try to import mollib and dies if not found.
try:
    import mollib
except ImportError:
    url = 'https://bitbucket.org/lvamparys/mollib'
    msg = 'module mollib not found - it can be downloaded from {}'.format(url)
    raise ImportError(msg)


requirements = [
    'netcdf4',
    'mollib'
]


setup(name='dock2nc',
      version='1.1.0',
      description='Convert ASCII docking files to netCDF.',
      long_description=readme + '\n\n' + history,
      author="Benoist LAURENT",
      author_email='benoist.laurent@ibpc.fr',
      # url='https://github.com/benoistlaurent/dock2nc',
      packages=['dock2nc'],
      package_dir={'dock2nc': 'dock2nc'},
      scripts=['scripts/dock2nc'],
      include_package_data=True,
      license="GPL",
      zip_safe=False,
      keywords='dock2nc',
      install_requires=requirements,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.0',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      # test_suite='tests',
      # tests_require=test_requirements,
      # entry_points={
      #     'console_scripts': [
      #         'oprpred = oprpred:main',
      #     ]
      # },
)
