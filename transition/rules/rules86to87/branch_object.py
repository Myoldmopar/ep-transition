from transition.rules import base_rule
from transition.idf.idfobject import IDFObject


class BranchTransitionRule(base_rule.TransitionRule):

    def get_name_of_object_to_transition(self):
        return "Branch"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):
        original_idf_fields = core_object.fields
        new_idf_fields = original_idf_fields
        new_idf_fields.insert(2, "NEW FIELD VALUE")
        print(core_object.object_name)
        print(new_idf_fields)
        new_branch_object = IDFObject([core_object.object_name] + new_idf_fields)
        # return a list since some transitions may split/add new objects
        return [new_branch_object]
