from eptransition.rules.base_rule import OutputVariableTransitionRule
from eptransition.rules.rules85to86.utilities import build_ref_pt_list
from eptransition.idf.objects import IDFObject


class Rule(OutputVariableTransitionRule):  # pragma no cover
    def get_output_objects(self):
        return self.original_full_variable_type_list()

    def get_standard_indexes_from_object(self, object_name):
        return self.original_standard_indexes_from_object(object_name)

    def get_complex_operation_types(self):
        return [self.OV]

    def get_simple_swaps(self):
        return {}

    def get_dependent_object_names(self):
        return ["DAYLIGHTING:DELIGHT:CONTROLS", "DAYLIGHTING:DELIGHT:REFERENCEPOINT"]

    def complex_output_operation(self, full_object, dependent_objects):
        if full_object.object_name.upper() == self.OV:
            # do daylighting stuff
            original_fields = full_object.fields
            new_fields = original_fields
            is_delight_out_var = False
            daylight_ref_pts = build_ref_pt_list(dependent_objects['DAYLIGHTING:DELIGHT:REFERENCEPOINT'],
                                                 dependent_objects['DAYLIGHTING:DELIGHT:CONTROLS'])
            if original_fields[0] != '*' and original_fields[1].startswith('Daylighting Reference Point'):
                for ref_pt in daylight_ref_pts:
                    if ref_pt.ref_pt_name.upper() == original_fields[0].upper():
                        is_delight_out_var = True
                        break
                if not is_delight_out_var:
                    new_fields[0] = original_fields[0] + '_DaylCtrl'
            if original_fields[0] != '*' and original_fields[1].startswith('Daylighting Lighting Power Multiplier'):
                for ref_pt in daylight_ref_pts:
                    if ref_pt.control_name.upper() == original_fields[0].upper():
                        is_delight_out_var = True
                        break
                if not is_delight_out_var:
                    new_fields[0] = original_fields[0] + '_DaylCtrl'
            new_object = IDFObject([full_object.object_name] + new_fields)
            return [new_object]
        else:  # pragma no cover
            # this section really isn't needed as this function is only called for registered types anyway
            return None
