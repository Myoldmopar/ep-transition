.. EnergyPlus Transition documentation master file, created by
   sphinx-quickstart on Fri Jan  6 16:14:11 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to EnergyPlus Python Transition's documentation!
========================================================

EnergyPlus Python Transition is a remake of the Fortran-based EnergyPlus file transition tool.  The purpose of this
tool is to transition an EnergyPlus input file from one version to the latest version.  Because the input forms change
between EnergyPlus versions so dramatically, having a tool like this is a mandatory piece of the EnergyPlus workflow.

The previous version, in Fortran, was difficult to maintain, as fewer and fewer Fortran developers remain.  In addition,
with the possibility of future input syntax changes (JSON), a new version transition tool was desired.  This version,
written in Python, is more modular in nature, with almost the entire code base written independent of any specific
version of EnergyPlus, and only the rules themselves plus 2 other lines needing to be modified for adding another
version.  The rules themselves are simply derived classes in Python that give clear guidance on writing new rules.

Installation:

Each tagged release of the software is posted to PyPi_.  With this in place, installation of the library into a given
Python installation is easy using pip::

  pip install eptransition

Once this is installed, it will copy the library into Python's appropriate package folder, and also create an executable
link to the main transition function, when possible, into the PATH, so that the eptransition script can be called
directly from the command line.  Usage of these two modes are described below.

.. _PyPi: https://pypi.python.org/pypi/eptransition/

Usage from Command Line:

Once installed, in order to execute the program from the command line, simply call the executable link created during
installation and pass in the input file(s) to transition::

  eptransition /path/to/idf /path/to/another/idf

Executing this command line will cause the tool to read the input file(s) first to find the start
version for each transition process.  The tool then checks whether this version is available and if so, reads appropriate
dictionary files for the start/end version, processes the IDF, executes all transition rules, and writes out a
transitioned input file.

Usage from Library:

Once installed, using from existing Python code is a simple matter.  Simply create a new Python script, and start by
importing the library::

  import eptransition

With the library imported, one can access all the underlying model structure, although the most likely usage will be
to programmatically transition files.  To do this, one can access the manager function directly::

  from eptransition.manager import TransitionManager
  for idf in ['/path/to/idf', 'path/to/another/idf']:
     tm = TransitionManager("/path/to/idf")
     try:
         tm.perform_transition()
     except Exception as e:
         print(e)

This is equivalent to the command line call above.

Class Structure:

.. toctree::
   :maxdepth: 2

   eptransition_transition
   eptransition_manager
   eptransition_exceptions
   eptransition_versions_versions
   eptransition_idd_objects
   eptransition_idd_processor
   eptransition_idf_objects
   eptransition_idf_processor
   eptransition_rules_baserule
   eptransition_rules_versionrule



Indexes and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

