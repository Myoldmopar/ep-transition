import os
import logging

from eptransition.exceptions import (
    FileAccessException as eFAE, FileTypeException as eFTE, ManagerProcessingException, ProcessingException
)
from eptransition.idd.processor import IDDProcessor
from eptransition.idf.objects import IDFStructure, ValidationIssue
from eptransition.idf.processor import IDFProcessor
from eptransition.rules.version_rule import VersionRule
from eptransition.versions.versions import TRANSITIONS, TypeEnum, FILE_TYPES


module_logger = logging.getLogger('eptransition.manager')


class TransitionManager(object):
    """
    This class is the main manager for performing a single transition of an input file from one version to another.

    Developer note: This class raises many exceptions, so logging.exception is handled at the level of the code
    calling these functions within a try/except block.  These functions do logging, but only the info/debug level.

    :param str original_input_file: Full path to the original idf to transition
    """
    def __init__(self, original_input_file):
        self.original_input_file = original_input_file
        module_logger.debug("Transitioning file: {}".format(original_input_file))
        self.new_input_file = self.original_input_file[:-4] + "_updated" + self.original_input_file[-4:]
        module_logger.debug("Created the new output file as {}".format(self.new_input_file))
        if os.path.exists(self.new_input_file):  # pragma no cover
            module_logger.debug("new_input_file path already exists, trying to remove!")
            os.remove(self.new_input_file)
            module_logger.debug("Successfully removed previous new_input_file")
        # instantiate to None for now
        self.original_idd_file = None
        self.new_idd_file = None

    def perform_transition(self):
        """
        This function manages the transition from one version to another by opening, validating, and writing files

        :return: 0 for success, raises exception for failures
        :raises FileAccessException: if a specified file does not access
        :raises FileTypeException: if a specified file type does not match the expected condition
        :raises ManagerProcessingException: if there is a problem processing the contents of the files
        """
        # Validate input file related things
        if not os.path.exists(self.original_input_file):  # pragma no cover
            raise eFAE(self.original_input_file, eFAE.CANNOT_FIND_FILE, eFAE.ORIGINAL_INPUT_FILE)
        if os.path.exists(self.new_input_file):  # pragma no cover
            raise eFAE(self.new_input_file, eFAE.FILE_EXISTS_MUST_DELETE, eFAE.UPDATED_INPUT_FILE)
        try:
            open(self.new_input_file, 'w').write('-')
        except:  # pragma no cover
            raise eFAE(self.new_input_file, eFAE.CANNOT_WRITE_TO_FILE, eFAE.UPDATED_INPUT_FILE)
        if self.original_input_file.endswith('.idf'):
            original_idf_file_type = TypeEnum.IDF
        elif self.original_input_file.endswith('.jdf'):  # pragma no cover
            original_idf_file_type = TypeEnum.JSON
        else:  # pragma no cover
            raise eFTE(self.original_input_file, eFTE.ORIGINAL_INPUT_FILE,
                       "Unexpected extension, should be .idf or .jdf")
        if self.new_input_file.endswith('.idf'):
            new_idf_file_type = TypeEnum.IDF
        elif self.new_input_file.endswith('.jdf'):  # pragma no cover
            new_idf_file_type = TypeEnum.JSON
        else:  # pragma no cover
            raise eFTE(self.new_input_file, eFTE.UPDATED_INPUT_FILE, "Unexpected extension, should be .idf or .jdf")

        # At this point we now need to know the version of the idf, before we even try to read the idd really
        original_idf_processor = IDFProcessor()
        try:
            # this call _will_ process the version into IDFObject.version_float or raise an exception if it fails
            idf_to_transition = original_idf_processor.process_file_given_file_path(self.original_input_file)
            module_logger.debug(
                "Successfully processed idf structure; found {} objects".format(len(idf_to_transition.objects)))
        except:  # pragma no cover
            raise ManagerProcessingException("Could not process original idf; aborting")

        # so we get the original idf version now
        original_idf_version = idf_to_transition.version_float
        module_logger.debug("Original IDF version found as {}".format(original_idf_version))

        # then we know which VERSION item we're working on:
        if original_idf_version in TRANSITIONS:
            # store the initial one
            first_transition = TRANSITIONS[original_idf_version]
            module_logger.debug("First transition to be attempted is from version {} to {}".format(
                first_transition.start_version, first_transition.end_version))
            # start the array of transitions
            these_transitions = [first_transition]
            # start the variable before we loop
            current_transition_end_version = first_transition.end_version
            while True:
                if current_transition_end_version in TRANSITIONS:
                    current_transition = TRANSITIONS[current_transition_end_version]
                    these_transitions.append(current_transition)
                    current_transition_end_version = current_transition.end_version
                    module_logger.debug("Follow-up transition found from version {} to {}".format(
                        current_transition.start_version, current_transition.end_version
                    ))
                    continue
                else:
                    break
        else:  # pragma no cover
            raise ManagerProcessingException(
                "IDF Version ({}) not found in available transitions".format(original_idf_version))

        for i, this_transition in enumerate(these_transitions):
            end_version = this_transition.end_version
            module_logger.debug("Found this version in transitions, will try to transition from {} to {}".format(
                this_transition.start_version, this_transition.end_version
            ))

            # if the IDD files are "None", then try to match them up
            idd_file = "Energy+.idd"
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            if self.original_idd_file is None:  # pragma no cover
                self.original_idd_file = os.path.join(cur_dir, "versions", str(this_transition.start_version), idd_file)
                module_logger.debug("Using \"original\" idd file at path: {}".format(self.original_idd_file))
            if self.new_idd_file is None:  # pragma no cover
                self.new_idd_file = os.path.join(cur_dir, "versions", str(this_transition.end_version), idd_file)
                module_logger.debug("Using \"new\" idd file at path: {}".format(self.new_idd_file))

            # Validate dictionary file things
            if not os.path.exists(self.original_idd_file):  # pragma no cover
                raise eFAE(self.original_idd_file, eFAE.CANNOT_FIND_FILE, eFAE.ORIGINAL_DICT_FILE)
            if not os.path.exists(self.new_idd_file):  # pragma no cover
                raise eFAE(self.new_idd_file, eFAE.CANNOT_FIND_FILE, eFAE.UPDATED_DICT_FILE)
            if self.original_idd_file.endswith('.idd'):
                original_idd_file_type = TypeEnum.IDF
            elif self.original_idd_file.endswith('.jdd'):  # pragma no cover
                original_idd_file_type = TypeEnum.JSON
            else:  # pragma no cover
                raise eFTE(self.original_idd_file, eFTE.ORIGINAL_DICT_FILE,
                           "Unexpected extension, should be .idd or .jdd")
            if self.new_idd_file.endswith('.idd'):
                new_idd_file_type = TypeEnum.IDF
            elif self.new_idd_file.endswith('.jdd'):  # pragma no cover
                new_idd_file_type = TypeEnum.JSON
            else:  # pragma no cover
                raise eFTE(self.new_idd_file, eFTE.UPDATED_DICT_FILE, "Unexpected extension, should be .idd or .jdd")

            # now validate the file types match each other
            if original_idf_file_type == original_idd_file_type:
                pass  # that's a good thing
            else:  # pragma no cover
                raise ManagerProcessingException("Original file types don't match; input file={}; dictionary={}".format(
                    original_idf_file_type, original_idd_file_type))

            end_type = FILE_TYPES[end_version]
            if new_idf_file_type == end_type and new_idd_file_type == end_type:
                pass  # that's a good thing
            else:  # pragma no cover
                raise ManagerProcessingException("Original file types don't match; input file={}; dictionary={}".format(
                    new_idf_file_type, new_idd_file_type))

            # and process the original idd file
            original_idd_processor = IDDProcessor()
            try:
                original_idd_structure = original_idd_processor.process_file_given_file_path(self.original_idd_file)
                module_logger.debug("Successfully processed original idd")
            except ProcessingException as e:  # pragma no cover
                raise ManagerProcessingException("Could not process original idd; message = " + str(e))

            # and process the new idd file
            new_idd_processor = IDDProcessor()
            try:
                new_idd_structure = new_idd_processor.process_file_given_file_path(self.new_idd_file)
                module_logger.debug("Successfully processed \"new\" idd")
            except:  # pragma no cover
                raise ManagerProcessingException("Could not process new idd; aborting")

            # validate the current idf before continuing
            issues = idf_to_transition.validate(original_idd_structure)
            if len(issues) > 0:  # pragma no cover
                for i in issues:
                    if i.severity == ValidationIssue.INFORMATION:
                        module_logger.debug(str(i))
                    elif i.severity == ValidationIssue.WARNING:
                        module_logger.warn(str(i))
                    elif i.severity == ValidationIssue.ERROR:
                        raise ManagerProcessingException(
                            "Errors found in validating of original idf against original idd; aborting", issues)

            class LocalRuleInformation:
                def __init__(self, local_rule):
                    self.dependent_names = local_rule.get_names_of_dependent_objects()
                    self.transition_function = local_rule.transition

            # now read in the rules and create a map based on the upper case version of the IDF object to transition
            this_version_rule = VersionRule(end_version)
            rules = [this_version_rule]
            rules.extend([x() for x in this_transition.transitions])
            rule_map = {}
            for rule in rules:
                rule_map[rule.get_name_of_object_to_transition().upper()] = LocalRuleInformation(rule)

            if this_transition.output_variable_transition is None:
                output_rule = None
                output_names = []
                module_logger.warn("This transition did not find an output variable transition class...you sure?")
            else:
                output_rule = this_transition.output_variable_transition()
                output_names = output_rule.get_output_objects()

            # create a list of objects to be deleted (which is a list of Type/Name, or more accurately Type/Field0
            objects_to_delete = []

            # create an intermediate list of idf objects to tentatively be written to the idf
            intermediate_idf_objects = []

            # create a final list of idf objects to actually be written to the idf
            final_idf_objects = []

            # loop over all objects in the original input file
            for original_idf_object in idf_to_transition.objects:
                idf_object_type_upper = original_idf_object.object_name.upper()
                # if the upper case version of this idf object is in the rule map, process the rule, otherwise just
                # keep the object in the intermediate list of objects to write
                if idf_object_type_upper in rule_map:
                    module_logger.debug("Transition object type: {}".format(idf_object_type_upper))
                    # retrieve the rule for this idf object
                    this_rule = rule_map[idf_object_type_upper]
                    # create a map of dependents; where the key is the upper case object type and the value is
                    # the list of all the objects found in the original idf
                    dependents = {}
                    for dep_idf_type in this_rule.dependent_names:
                        dependents[dep_idf_type.upper()] = idf_to_transition.get_idf_objects_by_type(dep_idf_type)
                    # call transition to actually perform object changes
                    transition_response = this_rule.transition_function(original_idf_object, dependents)
                    module_logger.debug(
                        "Object transition complete; # objects to write: {}; # objects to delete: {}".format(
                            len(transition_response.to_write), len(transition_response.to_delete)
                        ))
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
            module_logger.debug("First pass transition complete; # objects to delete: {}".format(len(objects_to_delete)))
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

            # report and done
            module_logger.debug("Transition complete; final # objects: {}".format(len(final_idf_structure.objects)))

            # but now...if we are going to cycle, we'll want the idf_to_transition variable to be filled
            # and if we are done, we'll write the file
            if i == len(these_transitions) - 1:
                module_logger.debug("Completed all transitions, writing file and leaving")
                final_idf_structure.write_idf(self.new_input_file, new_idd_structure)
            else:
                module_logger.debug("Going to start a new transition on this file, storing structure and continuing")
                idf_to_transition = final_idf_structure

        return 0
