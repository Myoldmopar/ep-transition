from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionReturn


class OutputVariableTransitionRule:
    def get_output_objects(self):
        return ["OUTPUT:VARIABLE", 'OUTPUT:METER', 'OUTPUT:METER:METERFILEONLY', 'OUTPUT:METER:CUMULATIVE',
                'OUTPUT:METER:CUMULATIVE:METERFILEONLY', 'OUTPUT:TABLE:TIMEBINS',
                'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITIMPORT:FROM:VARIABLE',
                'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITEXPORT:FROM:VARIABLE',
                'ENERGYMANAGEMENTSYSTEM:SENSOR', 'OUTPUT:TABLE:MONTHLY', 'METER:CUSTOM', 'METER:CUSTOMDECREMENT']

    def get_indeces_from_object(self, object_name):
        if object_name in ['OUTPUT:METER', 'OUTPUT:METER:METERFILEONLY', 'OUTPUT:METER:CUMULATIVE',
                           'OUTPUT:METER:CUMULATIVE:METERFILEONLY']:
            return [0]
        elif object_name in ['OUTPUT:VARIABLE', 'OUTPUT:TABLE:TIMEBINS',
                             'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITIMPORT:FROM:VARIABLE',
                             'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITEXPORT:FROM:VARIABLE']:
            return [1]
        elif object_name in ['ENERGYMANAGEMENTSYSTEM:SENSOR']:
            return [2]

    def get_new_output_variable(self, variable_name):
        if variable_name == 'SITE OUTDOOR AIR DRYBULB TEMPERATURE':
            return 'THAT THERE OUTSIDE HOTNESS RIGHT'

    def transition(self, core_object):
        original_idf_fields = core_object.fields
        new_idf_fields = original_idf_fields
        indeces = self.get_indeces_from_object(core_object.object_name.upper())
        for i in indeces:
            new_idf_fields[i] = self.get_new_output_variable(original_idf_fields[i].upper())
        new_variable_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_variable_object])
