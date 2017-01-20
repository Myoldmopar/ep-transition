from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "MaterialProperty:MoisturePenetrationDepth:Settings"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        original_idf_fields = core_object.fields
        new_idf_fields = [original_idf_fields[0]]
        old_field_2 = original_idf_fields[1]
        new_idf_fields.append("0.0")
        new_idf_fields.extend(original_idf_fields[2:6])
        new_idf_fields.append(old_field_2)
        new_idf_fields.extend(["0.0"] * 3)
        new_empd_object = IDFObject([core_object.object_name] + new_idf_fields)
        # return a list since some transitions may split/add new objects
        return TransitionReturn([new_empd_object])
