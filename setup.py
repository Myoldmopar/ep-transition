#!/usr/bin/env python

import codecs
import unittest
import os
import setuptools
import sys

from eptransition import __version__

if len(sys.argv) > 1:
    if sys.argv[1] == 'test':
        tests = unittest.TestLoader().discover('test')
        unittest.TextTestRunner().run(tests)

this_dir = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(this_dir, 'README.rst'), encoding='utf-8') as i_file:
    long_description = i_file.read()

setuptools.setup(
    name='eptransition',
    version=__version__,
    description='EnergyPlus file transition in Python.',
    long_description=long_description,
    url='https://github.com/myoldmopar/ep-transition',
    author='Edwin Lee',
    author_email='leeed2001@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    keywords='cli energyplus',
    packages=setuptools.find_packages(exclude=['test', 'test.*', '.tox']),
    install_requires=[],
    extras_require={
        'test': ['coverage', 'unittest', 'coveralls'],
    },
    entry_points={
        'console_scripts': [
            'eptransition=eptransition.transition:main',
        ],
    }
)
