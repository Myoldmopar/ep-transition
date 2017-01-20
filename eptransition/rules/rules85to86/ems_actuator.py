from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "EnergyManagementSystem:Actuator"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        # F4: Outdoor Air Dryblub Temperature, Outdoor Air Wetblub Temperature; correct spelling from "blub" to "bulb"
        original_idf_fields = core_object.fields
        new_idf_fields = original_idf_fields
        if original_idf_fields[3].upper() == "OUTDOOR AIR DRYBLUB TEMPERATURE":
            new_idf_fields[3] = "Outdoor Air Drybulb Temperature"
        elif original_idf_fields[3].upper() == "OUTDOOR AIR WETBLUB TEMPERATURE":
            new_idf_fields[3] = "Outdoor Air Wetbulb Temperature"
        new_equip_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_equip_object])
