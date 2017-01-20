from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "Exterior:FuelEquipment"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        # if F2 is Gas, change to "NaturalGas";   if F2 is LPG, change to "PropaneGas"
        original_idf_fields = core_object.fields
        new_idf_fields = original_idf_fields
        if original_idf_fields[1].upper() == "GAS":
            new_idf_fields[1] = "NaturalGas"
        elif original_idf_fields[1].upper() == "PROPANEGAS":
            new_idf_fields[1] = "PropaneGas"
        new_equip_object = IDFObject([core_object.object_name] + new_idf_fields)
        # return a list since some transitions may split/add new objects
        return TransitionReturn([new_equip_object])
