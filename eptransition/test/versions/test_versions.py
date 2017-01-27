import unittest

from eptransition.exceptions import ManagerProcessingException
from eptransition.versions.versions import TypeEnum, SingleTransition
from eptransition.rules.base_rule import TransitionRule, OutputVariableTransitionRule


class TestTypeEnums(unittest.TestCase):
    def test_they_exist(self):
        types = TypeEnum()
        attributes = dir(types)
        self.assertTrue("IDF" in attributes)
        self.assertTrue("JSON" in attributes)


class TestSingleTransition(unittest.TestCase):

    def test_valid(self):
        SingleTransition(1.0, 2.0, [TransitionRule()], OutputVariableTransitionRule(), None)

    def test_bad_start_version(self):
        with self.assertRaises(ManagerProcessingException):
            SingleTransition("abe", 2.0, [TransitionRule()], OutputVariableTransitionRule(), None)

    def test_bad_end_version(self):
        with self.assertRaises(ManagerProcessingException):
            SingleTransition(1.0, "abe", [TransitionRule()], OutputVariableTransitionRule(), None)

    def test_bad_transitions_type(self):
        with self.assertRaises(ManagerProcessingException):
            SingleTransition(1.0, 2.0, [TypeEnum()], OutputVariableTransitionRule(), None)

    def test_bad_output_type(self):
        with self.assertRaises(ManagerProcessingException):
            SingleTransition(1.0, 2.0, [TransitionRule()], TypeEnum(), None)

    def test_bad_global_type(self):
        with self.assertRaises(ManagerProcessingException):
            SingleTransition(1.0, 2.0, [TransitionRule()], OutputVariableTransitionRule(), TypeEnum())
