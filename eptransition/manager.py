from idd.processidd import IDDProcessor
from idf.idfobject import IDFStructure
from idf.processidf import IDFProcessor
from rules.rules86to87 import controller_list, branch


class TransitionManager(object):
    def __init__(self, original_input_file, new_input_file, original_idd_file, new_idd_file):
        self.original_input_file = original_input_file
        self.new_input_file = new_input_file
        self.original_idd_file = original_idd_file
        self.new_idd_file = new_idd_file

    def perform_transition(self):
        # self.input_file = input_file
        # if version.START_VERSION.file_type == TypeEnum.IDF:
        #     pass  # read as IDF
        #     # eventually we'll just infer the file types for in/out and act accordingly
        # TODO: Validate these files actually exist...and that you can write to new_input_file
        idf_processor = IDFProcessor()
        idf_structure = idf_processor.process_file_given_file_path(self.original_input_file)
        # original_idd_processor = IDDProcessor()
        # original_idd_structure = original_idd_processor.process_file_given_file_path(self.original_idd_file)
        # TODO: validate the current idf against the original IDD
        new_idd_processor = IDDProcessor()
        new_idd_structure = new_idd_processor.process_file_given_file_path(self.new_idd_file)
        rules = [branch.BranchTransitionRule(), controller_list.ControllerListTransitionRule()]
        rule_map = {}
        for rule in rules:
            rule_map[rule.get_name_of_object_to_transition().upper()] = [rule.get_names_of_dependent_objects(),
                                                                         rule.transition]
        objects_to_delete = []
        new_idf_objects = []
        for original_idf_object in idf_structure.objects:
            if original_idf_object.object_name.upper() in rule_map:
                this_rule = rule_map[original_idf_object.object_name.upper()]
                dependents = {}
                for dependent_idf_type in this_rule[0]:
                    dependents[dependent_idf_type.upper()] = idf_structure.get_idf_objects_by_type(dependent_idf_type)
                transition_response = this_rule[1](original_idf_object, dependents)
                new_idf_objects.extend(transition_response.to_write)
                objects_to_delete.extend(transition_response.to_delete)
            else:
                new_idf_objects.append(original_idf_object)
        delete_map = {}
        for object_to_delete in objects_to_delete:
            if object_to_delete.type.upper() in delete_map:
                delete_map[object_to_delete.type.upper()].append(object_to_delete.name.upper())
            else:
                delete_map[object_to_delete.type.upper()] = [object_to_delete.name.upper()]
        newer_idf_structure = IDFStructure("/newly/generated/idf")
        newer_idf_structure.objects = []
        for new_idf_object in new_idf_objects:
            delete = False
            if new_idf_object.object_name.upper() in delete_map:
                if new_idf_object.fields[0].upper() in delete_map[new_idf_object.object_name.upper()]:
                    delete = True
            if not delete:
                newer_idf_structure.objects.append(new_idf_object)
        newer_idf_structure.write_idf(self.new_input_file, new_idd_structure)
