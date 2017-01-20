from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "SetpointManager:SingleZone:Humidity:Minimum"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        # remove F2 and F3 [2] and [3] :  "Control Variable" and "Schedule Name"
        new_idf_fields = core_object.fields
        del new_idf_fields[1]  # remove F2, which is index 1
        del new_idf_fields[1]  # remove F3, which is index 1 since F2 was already removed
        new_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_object])


class Rule2(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "SetpointManager:SingleZone:Humidity:Maximum"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        # remove F2 and F3 [2] and [3] :  "Control Variable" and "Schedule Name"
        new_idf_fields = core_object.fields
        del new_idf_fields[1]  # remove F2, which is index 1
        del new_idf_fields[1]  # remove F3, which is index 1 since F2 was already removed
        new_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_object])
