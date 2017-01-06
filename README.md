# EnergyPlus Python Transition
Python version of the E+ input file transition utility

## Documentation [![](https://readthedocs.org/projects/energyplus-python-transition/badge/?version=latest)](http://energyplus-python-transition.readthedocs.org/en/latest/)
Documentation is hosted on [ReadTheDocs](http://energyplus-python-transition.readthedocs.org/en/latest/).  The docs are completely bare right now.  To build the documentation, enter the docs/ subdirectory and execute `make html`; then open `/docs/_build/html/index.html` to see the documentation.

## Testing [![](https://travis-ci.org/Myoldmopar/ep-transition.svg?branch=master)](https://travis-ci.org/Myoldmopar/ep-transition)
The source is tested using the python unittest framework.  To execute all the unit tests, just execute the test file (since it calls `unittest.main()`): `python test/test_main.py`.  The tests are also executed by [Travis CI](https://travis-ci.org/Myoldmopar/ep-transition).
