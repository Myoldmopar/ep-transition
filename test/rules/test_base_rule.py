import unittest

from eptransition.exceptions import UnimplementedMethodException
from eptransition.rules.base_rule import TransitionRule, OutputVariableTransitionRule, ObjectTypeAndName


class TestObjectTypeAndName(unittest.TestCase):
    def test_dumb_test(self):
        otn = ObjectTypeAndName('dumbtype', 'dumbname')
        self.assertEqual(otn.name, 'dumbname')
        self.assertEqual(otn.type, 'dumbtype')


class TestBaseRule(unittest.TestCase):
    def test_uninstantiatable(self):
        # calling the constructor is OK in case the derived class wants to always do this for good practice:
        r = TransitionRule()
        # but calling the other methods should throw exceptions
        with self.assertRaises(UnimplementedMethodException):
            r.get_name_of_object_to_transition()
        with self.assertRaises(UnimplementedMethodException):
            r.get_names_of_dependent_objects()
        with self.assertRaises(UnimplementedMethodException):
            r.transition(None, None)


class TestBaseOutputRule(unittest.TestCase):
    def test_uninstantiatable(self):
        # calling the constructor is OK in case the derived class wants to always do this for good practice:
        r = OutputVariableTransitionRule()
        # but calling the other methods should throw exceptions
        with self.assertRaises(UnimplementedMethodException):
            r.get_output_objects()
        with self.assertRaises(UnimplementedMethodException):
            r.get_standard_indexes_from_object(None)
        with self.assertRaises(UnimplementedMethodException):
            r.get_complex_operation_types()
        with self.assertRaises(UnimplementedMethodException):
            r.get_simple_swaps()
        with self.assertRaises(UnimplementedMethodException):
            r.complex_output_operation(None, None)
        # make sure the base object names returns a plain list
        self.assertEqual(r.get_dependent_object_names(), [])
