from eptransition.rules.base_rule import OutputVariableTransitionRule


class Rule(OutputVariableTransitionRule):

    def get_output_objects(self):
        return self.original_full_variable_type_list()

    def get_standard_indexes_from_object(self, object_name):
        return self.original_standard_indexes_from_object(object_name)

    def get_complex_operation_types(self):
        return [self.OM]

    def get_simple_swaps(self):
        return {
            'SITE OUTDOOR AIR DRYBULB TEMPERATURE': 'THAT THERE OUTSIDE HOTNESS RIGHT',
        }

    def complex_output_operation(self, full_object):
        if full_object.object_name.upper() == self.OM:
            # make up a fake output meter operation
            new_object = full_object
            new_object.object_name = "MAGICALOUTPUTDRAGON"
            return [new_object]
        else:  # pragma no cover
            # this section really isn't needed as this function is only called for registered types anyway
            return None
