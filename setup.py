#!/usr/bin/env python

from distutils.core import setup

setup(name='PyBilliards',
      version='0.1',
      description='A simple 2D billiards game',
      long_description='''A simple 2D billiards game written in python using pygame''',
      classifiers=['Topic :: Games/Entertainment',
                   'Topic :: Software Development :: Libraries :: pygame'],
      author='Prashant Agrawal & Pankaj Pandey',
      author_email='agrawal.prash@gmail.com,pankaj86@gmail.com',
      url='http://code.google.com/p/pybilliards/',
      package_dir = {'': 'src'},
      packages=['billiards'],
      package_data={'billiards': ['data/themes/*/*']},
      license = 'GPLv3+',
     )

