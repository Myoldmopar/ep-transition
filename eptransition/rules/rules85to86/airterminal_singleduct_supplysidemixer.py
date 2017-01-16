from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "AirTerminal:SingleDuct:SupplySideMixer"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        original_idf_fields = core_object.fields
        new_object_name = "AirTerminal:SingleDuct:Mixer"
        new_idf_fields = original_idf_fields
        new_idf_fields.insert(6, "SupplySide")
        new_mixer_object = IDFObject([new_object_name] + new_idf_fields)
        # return a list since some transitions may split/add new objects
        return TransitionReturn([new_mixer_object])
