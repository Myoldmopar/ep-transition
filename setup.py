#!/usr/bin/env python

import codecs
import unittest
import os
import setuptools

from eptransition import __version__


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('eptransition.test', pattern='test_*.py')
    print(str(test_suite))
    return test_suite

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
    },
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,

)
