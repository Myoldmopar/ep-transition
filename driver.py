#!/usr/bin/env python

import sys
import unittest

from transition.idf.idfobject import IDFStructure
from transition.idf.processidf import IDFProcessor
from transition.idd.processidd import IDDProcessor
from transition.rules.rules86to87.branch_object import BranchTransitionRule


class Argument:
    def __init__(self, cli_argument, num_additional_args, usage_hint):
        self.cli_argument = cli_argument
        self.num_additional_args = num_additional_args
        self.usage_hint = usage_hint


valid_args = [Argument('test', 0, ''),
              Argument('usage', 0, ''),
              Argument('update', 3, '<path/to/file/to/update> <path/to/original/idd> <path/to/new/idd>')]


def usage(test_mode=False):
    if not test_mode:  # pragma: no cover
        print("Usage: call with one of the following arguments:")
        for arg in valid_args:
            print("  " + sys.argv[0] + " " + arg.cli_argument + " " + arg.usage_hint)


def drive(argv, test_mode=False):
    # validate the argument list
    if len(argv) <= 1:
        if not test_mode:  # pragma: no cover
            print("Error: Must call with at least one command line argument!")
        usage(test_mode)
        return 1
    valid_keys = [a.cli_argument for a in valid_args]
    if argv[1] not in valid_keys:
        if not test_mode:  # pragma: no cover
            print("Error: Invalid command line argument passed in!")
            usage()
        return 1
    cur_arg = next((a for a in valid_args if a.cli_argument == argv[1]), None)
    if not cur_arg:  # pragma: no cover
        if not test_mode:
            print("Error: Unexpected error in processing command line arguments")
        usage(test_mode)
        return 1
    expected_total_argv = 2 + cur_arg.num_additional_args
    if len(argv) != expected_total_argv:
        if not test_mode:  # pragma: no cover
            print("Error: Invalid number of command line arguments")
        usage(test_mode)
        return 1
    # now do operations
    if argv[1] == valid_args[0].cli_argument:  # test
        tests = unittest.TestLoader().discover('test')
        unittest.TextTestRunner().run(tests)
    elif argv[1] == valid_args[1].cli_argument:  # usage
        if not test_mode:  # pragma: no cover
            usage()
    elif argv[1] == valid_args[2].cli_argument:  # update
        input_file = argv[2]
        idf_processor = IDFProcessor()
        idf_structure = idf_processor.process_file_given_file_path(input_file)
        original_idd_file = argv[3]
        original_idd_processor = IDDProcessor()
        original_idd_structure = original_idd_processor.process_file_given_file_path(original_idd_file)
        # TODO: validate the current idf against the original IDD
        new_idd_file = argv[4]
        new_idd_processor = IDDProcessor()
        new_idd_structure = new_idd_processor.process_file_given_file_path(new_idd_file)
        rules = [BranchTransitionRule()]
        rule_map = {}
        for rule in rules:
            rule_map[rule.get_name_of_object_to_transition().upper()] = [rule.get_names_of_dependent_objects(), rule.transition]
        new_idf_structure = IDFStructure("/newly/generated/idf")
        new_idf_structure.objects = []
        for original_idf_object in idf_structure.objects:
            if original_idf_object.object_name.upper() in rule_map:
                this_rule = rule_map[original_idf_object.object_name.upper()]
                dependents = {}
                for dependent_idf_type in this_rule[0]:
                    dependents[dependent_idf_type] = idf_structure.get_idf_objects_by_type(dependent_idf_type)
                new_idf_objects = this_rule[1](original_idf_object, dependents)
                new_idf_structure.objects.extend(new_idf_objects)
            else:
                new_idf_structure.objects.append(original_idf_object)
        new_idf_structure.write_idf(new_idd_structure)
    return 0


if __name__ == "__main__":
    sys.exit(drive(sys.argv))
