import logging

from eptransition.exceptions import UnimplementedMethodException
from eptransition.idf.objects import IDFObject


module_logger = logging.getLogger('eptransition.rules.base_rule')


class ObjectTypeAndName:
    """
    This is a simple class for defining an object type/name combination

    :param str object_type: The object type
    :param str object_name: The name of the object (usually field[0]
    """

    def __init__(self, object_type, object_name):
        self.type = object_type
        self.name = object_name


class TransitionReturn:
    """
    This is a simple class for capturing the response from a transition call

    :param [IDFObject] objects_to_write: The list of IDFObject instances to be written as a result of this transition
    :param [ObjectTypeAndName] objects_to_delete: The list of idf object type/name combinations to be deleted as a
                                                 result of this transition
    """

    def __init__(self, objects_to_write, objects_to_delete=None):
        self.to_write = objects_to_write
        if not objects_to_delete:
            objects_to_delete = []
        self.to_delete = objects_to_delete


class TransitionRule:
    """
    This class is a must-override base class for defining transition rules for idf objects
    """

    def __init__(self):
        pass

    def get_name_of_object_to_transition(self):
        """
        This method should be overridden in derived classes and return a single name of an object that this rule handles
        the transition for.

        :return: A string name of an object to transition
        :raises UnimplementedMethodException: Raised if this method is called on the base class itself
        """
        raise UnimplementedMethodException("TransitionRule", "get_name_of_object_to_transition")

    def get_names_of_dependent_objects(self):
        """
        This method should be overridden in derived classes and return a list of object names that the derived
        transition implementation is dependent upon.

        :return: A list of string object names
        :raises UnimplementedMethodException: Raised if this method is called on the base class itself
        """
        raise UnimplementedMethodException("TransitionRule", "get_names_of_dependent_objects")

    def transition(self, core_object, dependent_objects):
        """
        This method is the core transition operation for this object.

        :param core_object: The original idf object to be transitioned
        :param dependent_objects: A dictionary of {object_name: [idf_object, ...]} containing the idf object data in the
                                  original idf that have object names defined in this derived classes
                                  `get_names_of_dependent_objects` method.  Each key in this argument is a string
                                  object name, and each value is a list of all the idf objects in the file of that type.
        :return: A list of new IDFObject instances, typically just one though
        :raises UnimplementedMethodException: Raised if this method is called on the base class itself
        """
        raise UnimplementedMethodException("TransitionRule", "transition")


class OutputVariableTransitionRule:
    """
    This class is a must-override base class for defining transition rules for output variable objects
    These objects are treated somewhat specially by the tool because a small change can affect so
    many objects, and it would be unwise to expect each version to include so much repeated code.

    The structure of the output objects here is based on 8.5/8.6.  In the future, if the objects didn't change much,
    it would make most sense to just keep using this class and making small tweaks as needed.  If more major
    changes occur, it would be best to create a new base class to move forward.

    The fields for each object are described next

    - OV: Output:Variable

        0. Key Value
        1. Variable Name  * * * *
        2. Reporting Frequency
        3. Schedule Name

    - OM: Output:Meter, OMM: Output:Meter:MeterFileOnly

        0. Name  * * * *
        1. Reporting Frequency

    - OMC: Output:Meter:Cumulative, OMCM: Output:Meter:Cumulative:MeterFileOnly

        0. Name  * * * *
        1. Reporting Frequency

    - OTT: Output:Table:TimeBins

        0. Key Value
        1. Variable Name  * * * *
        2. Interval Start
        3. Interval Size
        4. Interval Count
        5. Schedule Name
        6. Variable Type

    - FMUI: ExternalInterface:FunctionalMockupUnitImport:From:Variable

        0. EnergyPlus Key Value
        1. EnergyPlus Variable Name  * * * *
        2. FMU File Name
        3. FMU Instance Name
        4. FMU Variable Name

    - FMUE: ExternalInterface:FunctionalMockupUnitExport:From:Variable

        0. EnergyPlus Key Value
        1. EnergyPlus Variable Name  * * * *
        2. FMU Variable Name

    - EMS: EnergyManagementSystem:Sensor

        0. Name
        1. Output:Variable or Output:Meter Key Name
        2. Output:Variable or Output:Meter Name  * * * *

    - OTM: Output:Table:Monthly

        0. Name
        1. Digits after Decimal
        2. Variable or Meter X Name  * * * *
        3. Variable or Meter X Aggregation Type

        ... repeating with variable names for each 2, 4, 6, 8, ...

    - OTA: Output:Table:Annual

        0. Name
        1. Filter
        2. Schedule Name
        3. Variable or Meter X Name  * * * *
        4. Variable or Meter X Aggregation Type

        ... repeating with variable names for each 3, 5, 7, 9, ...

    - MC: Meter:Custom

        0. Name
        1. Fuel Type
        2. Key Name X
        3. Output Variable or Meter Name X  * * * *

        ... repeating with variable names for each 3, 5, 7, 9, ...

    - MCD: Meter:CustomDecrement

        0. Name
        1. Fuel Type
        2. Source Meter Name  ????
        3. Key Name X
        4. Output Variable or Meter Name X

        ... repeating with variable names for each 4, 6, 8, 10, ...

    """

    # convenience constants
    OV = 'OUTPUT:VARIABLE'
    OM = 'OUTPUT:METER'
    OMM = 'OUTPUT:METER:METERFILEONLY'
    OMC = 'OUTPUT:METER:CUMULATIVE'
    OMCM = 'OUTPUT:METER:CUMULATIVE:METERFILEONLY'
    OTT = 'OUTPUT:TABLE:TIMEBINS'
    FMUI = 'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITIMPORT:FROM:VARIABLE'
    FMUE = 'EXTERNALINTERFACE:FUNCTIONALMOCKUPUNITEXPORT:FROM:VARIABLE'
    EMS = 'ENERGYMANAGEMENTSYSTEM:SENSOR'
    OTM = 'OUTPUT:TABLE:MONTHLY'
    OTA = 'OUTPUT:TABLE:ANNUAL'
    MC = 'METER:CUSTOM'
    MCD = 'METER:CUSTOMDECREMENT'

    def __init__(self):
        pass

    def original_full_variable_type_list(self):
        # set strings to be used by derived classes for convenience
        return [self.OV, self.OM, self.OMM, self.OMC, self.OMCM, self.OTT,
                self.FMUI, self.FMUE, self.EMS, self.OTM, self.MC, self.MCD]

    def original_standard_indexes_from_object(self, object_name):
        """
        This method returns the list of indexes where variable names are found.  These are zero based indexes.  This
        method returns a base version that can be used by a derived class directly, modified, or used as a template
        for future derived classes.

        :param object_name: The upper case name of the object currently being transitioned.
        :return: A list of zero-based indexes
        """
        if object_name in [self.OM, self.OMM, self.OMC, self.OMCM]:
            return [0]
        elif object_name in [self.OV, self.OTT, self.FMUE, self.FMUI]:
            return [1]
        elif object_name in [self.EMS]:
            return [2]
        elif object_name in [self.OTM]:  # pragma no cover -- will add back in once we test an idf that has OTM
            return range(2, 100, 2)
        elif object_name in [self.OTA, self.MC]:  # pragma no cover -- will add back in once we test in idf that has OTA
            return range(3, 100, 2)
        elif object_name in [self.MCD]:  # pragma no cover -- will add back in once we test in idf that has MCD
            return range(4, 100, 2)

    def get_output_objects(self):
        """
        This method should be overridden in derived classes and return a list of all output-related object types
        in this version of EnergyPlus.  A base version is available in the base class that can be used as a starter
        and if an object name changes, the derived class can change that name as needed in the return array.

        :return: A list of strings, each representing an output object type name
        :raises UnimplementedMethodException: Raised if this method is called on the base class itself
        """
        raise UnimplementedMethodException("OutputVariableTransitionRule", "get_output_objects")

    def get_standard_indexes_from_object(self, object_name):
        """
        This method should be overridden in derived classes and return a list of the zero-based field indexes that
        include a variable name in the given object type.  A base version is available in the base class that can be
        used as a starter and if the structure of any object types changes, the derived class can change that one as
        needed in the return list

        :param object_name: The name of the object being inspected
        :return: A list of zero-based indexes, each representing a field containing an output variable name
        :raises UnimplementedMethodException: Raised if this method is called on the base class itself
        """
        raise UnimplementedMethodException("OutputVariableTransitionRule", "get_standard_indexes_from_object")

    def get_complex_operation_types(self):
        """
        This method should be overridden in the derived classes and return a list of object names that require more
        complex transition operations than a simple variable name swap

        :return: A list of strings, each representing an object name that requires complex transition operations
        :raises UnimplementedMethodException: Raised if this method is called on the base class itself
        """
        raise UnimplementedMethodException("OutputVariableTransitionRule", "get_complex_operation_types")

    def get_simple_swaps(self):
        """
        This method should be overridden in derived classes and return a dictionary where each key is the name of
        an output variable, and the value of each key is the new variable name.  This map is used when doing the
        simple variable name swaps.

        :return: A dictionary of <old_variable_name, new_variable_name>
        :raises UnimplementedMethodException: Raised if this method is called on the base class itself
        """
        raise UnimplementedMethodException("OutputVariableTransitionRule", "get_simple_swaps")

    def simple_name_swap(self, variable_name):
        """
        This method is a simple method that queries the *must-override* `get_simple_swaps` method in the derived class
        and either returns a new variable name to swap in place of the original name, or returns None as a signal that
        this original variable name does not need replacement

        :param variable_name: The original variable name to potentially be replaced
        :return: A new variable name, if a swap is to be performed, or None if not
        """
        swaps = self.get_simple_swaps()
        if variable_name in swaps:
            return swaps[variable_name]
        else:
            return None

    def complex_output_operation(self, full_object):
        """
        This method should be overridden in derived classes and should perform the complex operations to transition
        the argument object passed in.  The function should return a list because some complex operations may split the
        initial object into multiple objects.  The object passed in will have any simple name swaps already performed.

        :param full_object: The original object to be replaced.
        :return: A list of new IDFObject instances, typically just one though
        :raises UnimplementedMethodException: Raised if this method is called on the base class itself
        """
        raise UnimplementedMethodException("OutputVariableTransitionRule", "complex_output_operation")

    def transition(self, core_object):
        """
        This method can be implemented by derived classes if necessary, but should capture the entire transition
        functionality just using the other required <must-override> methods in this class.  This function first scans
        all the variable names in the current locations, and renames as needed.  Then this function checks if
        this object type needs a complex transition, and if so, calls the appropriate derived method.  This method then
        returns a full IDFObject instance.

        :param core_object: The original object to be replaced
        :return: A list of new IDFObject instances, typically just one though
        """
        original_idf_fields = core_object.fields
        obj_name_upper = core_object.object_name.upper()
        # first just copy all fields into a new list
        new_idf_fields = original_idf_fields
        # then go through and do simple renames of the variables in the expected locations
        indexes = self.get_standard_indexes_from_object(obj_name_upper)
        if indexes is None:
            module_logger.warn("no indexes for output object: {}".format(core_object.object_name))  # pragma no cover
        else:
            for i in indexes:
                try:
                    original_idf_fields[i]
                except IndexError:  # pragma no cover   this could be covered if the idf tests were larger
                    break
                maybe_new_name = self.simple_name_swap(original_idf_fields[i].upper())
                if maybe_new_name:
                    new_idf_fields[i] = maybe_new_name
        # and create a temporary object
        new_variable_object = IDFObject([core_object.object_name] + new_idf_fields)
        # then do complex operations if needed
        if obj_name_upper in self.get_complex_operation_types():
            new_variable_objects = self.complex_output_operation(new_variable_object)
        else:
            new_variable_objects = [new_variable_object]
        # and finally return whatever we ended up with
        return TransitionReturn(new_variable_objects)
