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


setup(name='dock2nc',
      version='1.0.0',
      description='Convert ASCII docking files to netCDF.',
      author='Benoist LAURENT',
      author_email='benoist.laurent@ibpc.fr',
      packages=['dock2nc'],
      scripts=['scripts/dock2nc'],
      license='GPL')


setup(name='dock2nc',
      version='1.0.0',
      description='Convert ASCII docking files to netCDF.',
      long_description=readme + '\n\n' + history,
      author="Benoist LAURENT",
      author_email='benoist.laurent@ibpc.fr',
      # url='https://github.com/benoistlaurent/dock2nc',
      packages=['dock2nc'],
      package_dir={'dock2nc': 'dock2nc'},
      include_package_data=True,
      license="GPL",
      zip_safe=False,
      keywords='oprpred',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
      ],
      # test_suite='tests',
      # tests_require=test_requirements,
      # entry_points={
      #     'console_scripts': [
      #         'oprpred = oprpred:main',
      #     ]
      # },
      data_files=[(etc_dir, ['etc/rules.txt'])]
)
