from unittest import TestCase

from eptransition.epexceptions import UnimplementedMethodException
from eptransition.rules.base_rule import TransitionRule


class TestBaseRule(TestCase):
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
