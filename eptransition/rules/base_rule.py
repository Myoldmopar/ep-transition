from eptransition.exceptions import UnimplementedMethodException
from eptransition.idf.objects import IDFObject


class ObjectTypeAndName:
    """
    This is a simple init only class for defining an object type/name combination

    :param str object_type: The object type
    :param str object_name: The name of the object (usually field[0]
    """
    def __init__(self, object_type, object_name):
        self.type = object_type
        self.name = object_name


class TransitionReturn:
    """
    This is a simple init only class for capturing the response from a transition call

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
        """
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override get_name_of_object_to_transition() method")

    def get_names_of_dependent_objects(self):
        """
        This method should be overridden in derived classes and return a list of object names that the derived
        transition implementation is dependent upon.

        :return: A list of string object names
        """
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override get_names_of_dependent_objects() method")

    def transition(self, core_object, dependent_objects):
        """
        This method is the core transition operation for this object.

        :param core_object: The original idf object to be transitioned
        :param dependent_objects: A dictionary of {object_name: [idf_object, ...]} containing the idf object data in the
                                  original idf that have object names defined in this derived classes
                                  `get_names_of_dependent_objects` method.  Each key in this argument is a string
                                  object name, and each value is a list of all the idf objects in the file of that type.
        :return: A list of new IDFObject instances, typically just one though
        """
        raise UnimplementedMethodException(
            "TransitionRule derived classes should override transition() method")


class OutputVariableTransitionRule:
    """
    This class is a must-override base class for defining transition rules for output variable objects
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
        elif object_name in [self.OTM]:  # pragma no cover   -- will add back in once we test an idf that has OTM
            return range(2, 100, 2)

    def get_output_objects(self):
        """
        This method should be overridden in derived classes and return a list of all output-related object types
        in this version of EnergyPlus.  A base version is available in the base class that can be used as a starter
        and if an object name changes, the derived class can change that name as needed in the return array.

        :return: A list of strings, each representing an output object type name
        """
        raise UnimplementedMethodException(
            "OutputVariableTransitionRule derived classes should override get_output_objects() method")

    def get_standard_indexes_from_object(self, object_name):
        """
        This method should be overridden in derived classes and return a list of the zero-based field indexes that
        include a variable name in the given object type.  A base version is available in the base class that can be
        used as a starter and if the structure of any object types changes, the derived class can change that one as
        needed in the return list

        :param object_name: The name of the object being inspected
        :return: A list of zero-based indexes, each representing a field containing an output variable name
        """
        raise UnimplementedMethodException(
            "OutputVariableTransitionRule derived classes should override get_standard_indexes_from_object() method")

    def get_complex_operation_types(self):
        """
        This method should be overridden in the derived classes and return a list of object names that require more
        complex transition operations than a simple variable name swap

        :return: A list of strings, each representing an object name that requires complex transition operations
        """
        raise UnimplementedMethodException(
            "OutputVariableTransitionRule derived classes should override get_complex_operation_types() method")

    def get_simple_swaps(self):
        """
        This method should be overridden in derived classes and return a dictionary where each key is the name of
        an output variable, and the value of each key is the new variable name.  This map is used when doing the
        simple variable name swaps.

        :return: A dictionary of <old_variable_name, new_variable_name>
        """
        raise UnimplementedMethodException(
            "OutputVariableTransitionRule derived classes should override get_simple_swaps() method")

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
        """
        raise UnimplementedMethodException(
            "OutputVariableTransitionRule derived classes should override complex_output_operation() method")

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
