from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):

    def __init__(self, object_name, zero_based_field_index_to_remove):
        TransitionRule.__init__(self)
        self.object_name = object_name
        self.field_to_remove = zero_based_field_index_to_remove

    def get_name_of_object_to_transition(self):
        return self.object_name

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        new_idf_fields = core_object.fields
        del new_idf_fields[self.field_to_remove]
        new_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_object])
