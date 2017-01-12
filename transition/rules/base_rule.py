from transition.exceptions import UnimplementedMethodException


class TransitionRule:

    def get_name_of_object_to_transition(self):
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override get_name_of_object_to_transition() method")

    def get_names_of_dependent_objects(self):
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override get_names_of_dependent_objects() method")

    def transition(self, core_object, dependent_objects):
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override transition() method")
