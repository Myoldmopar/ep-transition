import os

from eptransition.exceptions import (
    FileAccessException, FileTypeException, ManagerProcessingException, ProcessingException
)
from eptransition.idd.processor import IDDProcessor
from eptransition.idf.objects import IDFStructure
from eptransition.idf.processor import IDFProcessor
from eptransition.rules.version_rule import VersionRule
from eptransition.versions import VERSIONS, TypeEnum


class TransitionManager(object):
    """
    This class is the main manager for performing a single transition of an input file from one version to another.

    :param float start_version: A floating point representation of the major.minor version number of the
                                starting EnergyPlus version for this transition
    :param float end_version: A floating point representation of the major.minor version number of the
                              ending EnergyPlus version for this transition
    :param str original_input_file: Full path to the original idf to transition
    :param str new_input_file: Full path to the final (transitioned) idf
    :param str original_idd_file: Full path to the idd file for the original, starting, EnergyPlus version
    :param str new_idd_file: Full path to the idd file for the final, ending, EnergyPlus version
    """
    def __init__(self, start_version, end_version, original_input_file,
                 new_input_file, original_idd_file, new_idd_file):
        # TODO: Trap for bad start/end version arguments
        self.start_version = VERSIONS[start_version]
        self.end_version = VERSIONS[end_version]
        self.original_input_file = original_input_file
        self.new_input_file = new_input_file
        self.original_idd_file = original_idd_file
        self.new_idd_file = new_idd_file

    def perform_transition(self):
        """
        This function manages the transition from one version to another by opening, validating, and writing files

        :return: SHOULD RETURN SOMETHING
        """
        # TODO: Return something
        # Validate file path things
        if not os.path.exists(self.original_input_file):  # pragma no cover
            raise FileAccessException(
                "Could not access original input file at path = \"" + self.original_input_file + "\"")
        if not os.path.exists(self.original_idd_file):  # pragma no cover
            raise FileAccessException(
                "Could not access original IDD file at path = \"" + self.original_idd_file + "\"")
        if not os.path.exists(self.new_idd_file):  # pragma no cover
            raise FileAccessException(
                "Could not access updated IDD file at path = \"" + self.new_idd_file + "\"")
        if os.path.exists(self.new_input_file):  # pragma no cover
            raise FileAccessException(
                "Updated input file already exists at = \"" + self.new_input_file + "\"; remove before running!")
        try:
            open(self.new_input_file, 'w').write('-')
        except:  # pragma no cover
            raise FileAccessException(
                "Could not write to updated file name at = \"" + self.new_input_file + "\"; aborting!")

        # Check file types
        if self.original_input_file.endswith('.idf'):
            original_idf_file_type = TypeEnum.IDF
        elif self.original_input_file.endswith('.jdf'):  # pragma no cover
            original_idf_file_type = TypeEnum.JSON
        else:  # pragma no cover
            raise FileTypeException("Original input file path has unexpected extension, should be .idf or .jdf")
        if self.new_input_file.endswith('.idf'):
            new_idf_file_type = TypeEnum.IDF
        elif self.new_input_file.endswith('.jdf'):  # pragma no cover
            new_idf_file_type = TypeEnum.JSON
        else:  # pragma no cover
            raise FileTypeException("New input file path has unexpected extension, should be .idf or .jdf")
        if self.original_idd_file.endswith('.idd'):
            original_idd_file_type = TypeEnum.IDF
        elif self.original_idd_file.endswith('.jdd'):  # pragma no cover
            original_idd_file_type = TypeEnum.JSON
        else:  # pragma no cover
            raise FileTypeException("Original input dictionary path has unexpected extension, should be .idd or .jdd")
        if self.new_idd_file.endswith('.idd'):
            new_idd_file_type = TypeEnum.IDF
        elif self.new_idd_file.endswith('.jdd'):  # pragma no cover
            new_idd_file_type = TypeEnum.JSON
        else:  # pragma no cover
            raise FileTypeException("New input dictionary path has unexpected extension, should be .idd or .jdd")

        # now validate the file types
        start_type = self.start_version.file_type
        if original_idf_file_type == start_type and original_idd_file_type == start_type:
            pass  # that's a good thing
        else:  # pragma no cover
            raise FileTypeException("Original files don't match expected version file type; expected: " +
                                    self.start_version.file_type)
        end_type = self.end_version.file_type
        if new_idf_file_type == end_type and new_idd_file_type == end_type:
            pass  # that's a good thing
        else:  # pragma no cover
            raise FileTypeException("Updated files don't match expected version file type; expected: " +
                                    self.end_version.file_type)

        # process the original input file
        original_idf_processor = IDFProcessor()
        try:
            original_idf_structure = original_idf_processor.process_file_given_file_path(self.original_input_file)
        except:  # pragma no cover
            raise ManagerProcessingException("Could not process original idf; aborting")

        # and process the original idd file
        original_idd_processor = IDDProcessor()
        try:
            original_idd_structure = original_idd_processor.process_file_given_file_path(self.original_idd_file)
        except ProcessingException as e:  # pragma no cover
            raise ManagerProcessingException("Could not process original idd; message = " + str(e))

        # and process the new idd file
        new_idd_processor = IDDProcessor()
        try:
            new_idd_structure = new_idd_processor.process_file_given_file_path(self.new_idd_file)
        except:  # pragma no cover
            raise ManagerProcessingException("Could not process new idd; aborting")

        # validate the current idf before continuing
        issues = original_idf_structure.validate(original_idd_structure)
        if len(issues) > 0:  # pragma no cover
            # TODO: Once issues have severities, just check for fatal errors
            raise ManagerProcessingException(
                "Issues found in validating of original idf against original idd; aborting")

        # check the version of the original idf
        if original_idf_structure.version_float != self.start_version.version:  # pragma no cover
            raise ManagerProcessingException(
                "Input file version does not match expected.  (expected={};found={})".format(
                    self.start_version.version, original_idf_structure.version_float))

        class LocalRuleInformation:
            def __init__(self, local_rule):
                self.dependent_names = local_rule.get_names_of_dependent_objects()
                self.transition_function = local_rule.transition

        # now read in the rules and create a map based on the upper case version of the IDF object to transition
        this_version_rule = VersionRule(self.end_version)
        rules = [this_version_rule]
        rules.extend([x() for x in self.end_version.transitions])
        rule_map = {}
        for rule in rules:
            rule_map[rule.get_name_of_object_to_transition().upper()] = LocalRuleInformation(rule)

        if self.end_version.output_variable_transition is None:
            output_rule = None
            output_names = []
        else:
            output_rule = self.end_version.output_variable_transition()
            output_names = output_rule.get_output_objects()

        # create a list of objects to be deleted (which is a list of Type/Name, or more accurately Type/Field0
        objects_to_delete = []

        # create an intermediate list of idf objects to tentatively be written to the idf
        intermediate_idf_objects = []

        # create a final list of idf objects to actually be written to the idf
        final_idf_objects = []

        # loop over all objects in the original input file
        for original_idf_object in original_idf_structure.objects:
            idf_object_type_upper = original_idf_object.object_name.upper()
            # if the upper case version of this idf object is in the rule map, process the rule, otherwise just
            # keep the object in the intermediate list of objects to write
            if idf_object_type_upper in rule_map:
                # retrieve the rule for this idf object
                this_rule = rule_map[idf_object_type_upper]
                # create a map of dependents; where the key is the upper case object type and the value is
                # the list of all the objects found in the original idf
                dependents = {}
                for dep_idf_type in this_rule.dependent_names:
                    dependents[dep_idf_type.upper()] = original_idf_structure.get_idf_objects_by_type(dep_idf_type)
                # call transition to actually perform object changes
                transition_response = this_rule.transition_function(original_idf_object, dependents)
                # extend the intermediate list objects with changed things and the delete list with things to delete
                intermediate_idf_objects.extend(transition_response.to_write)
                objects_to_delete.extend(transition_response.to_delete)
            elif idf_object_type_upper in output_names:
                transition_response = output_rule.transition(original_idf_object)
                intermediate_idf_objects.extend(transition_response.to_write)
            else:
                # if there was no rule, just keep the object as it is
                intermediate_idf_objects.append(original_idf_object)

        # create a map of objects to delete based on type
        delete_map = {}
        for object_to_delete in objects_to_delete:
            object_type_upper = object_to_delete.type.upper()
            object_name_upper = object_to_delete.name.upper()
            if object_type_upper in delete_map:
                delete_map[object_type_upper].append(object_name_upper)
            else:
                delete_map[object_type_upper] = [object_name_upper]

        # and now we write out the final idf structure
        final_idf_structure = IDFStructure(self.new_input_file)

        # loop over all
        for intermediate_idf_object in intermediate_idf_objects:
            delete = False
            if intermediate_idf_object.object_name.upper() in delete_map:
                if intermediate_idf_object.fields[0].upper() in delete_map[intermediate_idf_object.object_name.upper()]:
                    delete = True
            if not delete:
                final_idf_objects.append(intermediate_idf_object)
        final_idf_structure.objects = final_idf_objects
        final_idf_structure.write_idf(self.new_input_file, new_idd_structure)
