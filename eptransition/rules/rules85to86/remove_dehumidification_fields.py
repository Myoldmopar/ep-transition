from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "HVACTemplate:System:UnitarySystem"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        # remove F57 = [56] : Dehumidifaction Control Zone Name
        new_idf_fields = core_object.fields
        del new_idf_fields[56]
        new_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_object])


class Rule2(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "HVACTemplate:System:Unitary"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        # remove F40 = [39] : Dehumidifaction Control Zone Name
        new_idf_fields = core_object.fields
        del new_idf_fields[39]
        new_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_object])
