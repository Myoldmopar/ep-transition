from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "ChillerHeater:Absorption:DirectFired"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        # remove F33 = [32] : Chiller Flow Mode
        new_idf_fields = core_object.fields
        del new_idf_fields[32]
        new_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_object])
