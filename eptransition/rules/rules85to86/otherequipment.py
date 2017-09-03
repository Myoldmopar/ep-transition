from pyiddidf.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "OtherEquipment"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        original_idf_fields = core_object.fields
        # need to just add a new field F2, (index 1 here), blank
        new_idf_fields = original_idf_fields
        new_idf_fields.insert(1, "")
        new_equip_object = IDFObject([core_object.object_name] + new_idf_fields)
        # return a list since some transitions may split/add new objects
        return TransitionReturn([new_equip_object])
