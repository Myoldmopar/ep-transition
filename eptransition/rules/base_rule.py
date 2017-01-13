from eptransition.epexceptions import UnimplementedMethodException


class ObjectTypeAndName:
    def __init__(self, object_type, object_name):
        self.type = object_type
        self.name = object_name


class TransitionReturn:
    def __init__(self, objects_to_write, objects_to_delete=None):
        self.to_write = objects_to_write
        if not objects_to_delete:
            objects_to_delete = []
        self.to_delete = objects_to_delete


class TransitionRule:
    def __init__(self):
        pass

    def get_name_of_object_to_transition(self):
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override get_name_of_object_to_transition() method")

    def get_names_of_dependent_objects(self):
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override get_names_of_dependent_objects() method")

    def transition(self, core_object, dependent_objects):
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override eptransition() method")
