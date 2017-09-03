#!/usr/bin/env python

import setuptools

import eptransition

setuptools.setup(
    name='eptransition',
    version=eptransition.__version__,
    description='EnergyPlus file transition in Python.',
    long_description=open('README.rst').read(),
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
    include_package_data=True,
    install_requires=['pyiddidf==0.5'],
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
)
