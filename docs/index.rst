.. EnergyPlus Transition documentation master file, created by
   sphinx-quickstart on Fri Jan  6 16:14:11 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to EnergyPlus Python Transition's documentation!
========================================================

EnergyPlus Python Transition is a remake of the Fortran-based EnergyPlus file transition tool.  The purpose of this
tool is to transition an EnergyPlus input file from one version to another.  Because the input forms change between
EnergyPlus versions so dramatically, having a tool like this is a mandatory piece of the EnergyPlus workflow.

The previous version, in Fortran, was difficult to maintain, as fewer and fewer Fortran developers remain.  In addition,
with the possibility of future input syntax changes (JSON), a new version transition tool was desired.  This version,
written in Python, is more modular in nature, with almost the entire codebase written independent of any specific
version of EnergyPlus, and only the rules themselves plus 2 other lines needing to be modified for adding another
version.  The rules themselves are simply derived classes in Python that give clear guidance on writing new rules.

Contents:

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



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

