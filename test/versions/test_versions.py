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

    def test_start_version(self):
        SingleTransition(1.0, 2.0, [TransitionRule()], OutputVariableTransitionRule())
        with self.assertRaises(ManagerProcessingException):
            SingleTransition("abe", 2.0, [TransitionRule()], OutputVariableTransitionRule())

    def test_end_version(self):
        SingleTransition(1.0, 2.0, [TransitionRule()], OutputVariableTransitionRule())
        with self.assertRaises(ManagerProcessingException):
            SingleTransition(1.0, "abe", [TransitionRule()], OutputVariableTransitionRule())

    def test_transitions(self):
        SingleTransition(1.0, 2.0, [TransitionRule()], OutputVariableTransitionRule())
        with self.assertRaises(ManagerProcessingException):
            SingleTransition(1.0, 2.0, [TypeEnum()], OutputVariableTransitionRule())

    def test_output(self):
        SingleTransition(1.0, 2.0, [TransitionRule()], OutputVariableTransitionRule())
        with self.assertRaises(ManagerProcessingException):
            SingleTransition(1.0, 2.0, [TransitionRule()], TypeEnum())
