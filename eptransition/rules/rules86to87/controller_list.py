from eptransition.idf.idfobject import IDFObject
from eptransition.rules.base_rule import ObjectTypeAndName, TransitionRule, TransitionReturn


class ControllerListTransitionRule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "AirLoopHVAC:ControllerList"

    def get_names_of_dependent_objects(self):
        return ["Controller:OutdoorAir"]

    def transition(self, core_object, dependent_objects):
        oa_controllers = dependent_objects["CONTROLLER:OUTDOORAIR"]
        # could look up things in dependent objects in order to make a decision
        original_idf_fields = core_object.fields
        # find the matching OA controller by name
        objects_to_delete = []
        random_field = ""
        for oac in oa_controllers:
            if oac.fields[0].upper() == original_idf_fields[2].upper():
                random_field = oac.fields[7]
                objects_to_delete.append(ObjectTypeAndName("OUTDOORAIR:NODE", oac.fields[4]))
                objects_to_delete.append(ObjectTypeAndName("OUTDOORAIR:NODE", oac.fields[3]))
        new_idf_fields = original_idf_fields
        new_idf_fields[2] = random_field
        new_controller_list_object = IDFObject([core_object.object_name] + new_idf_fields)
        # return a list since some transitions may split/add new objects
        objects_to_write = [new_controller_list_object]
        return TransitionReturn(objects_to_write, objects_to_delete)
