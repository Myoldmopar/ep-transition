from codecs import open
from os.path import abspath, dirname, join

from setuptools import setup, find_packages

from eptransition import __version__, driver

import sys
if len(sys.argv) > 1:
    if sys.argv[1] == 'test':
        sys.exit(driver.drive(sys.argv))

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README'), encoding='utf-8') as file:
    long_description = file.read()

setup(
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
    packages=find_packages(exclude=['test', 'support', 'build', '.tox', 'dist', 'docs', 'scripts']),
    install_requires=[],
    extras_require={
        'test': ['coverage', 'unittest', 'coveralls'],
    },
    entry_points={
        'console_scripts': [
            'eptransition=eptransition.driver:drive_from_cmdline',
        ],
    }
)
