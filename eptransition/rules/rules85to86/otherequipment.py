from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "Branch"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        original_idf_fields = core_object.fields
        # we need to remove F2, F8, F13, F18, ....
        # these would be, zero based, 1, 7, 12, 17, 22, ....
        indeces_to_remove = [1]
        num_fields = len(core_object.fields)
        i_to_remove = 7
        while True:
            i_to_remove += 5
            if i_to_remove < num_fields:  # pragma no cover
                indeces_to_remove.append(i_to_remove)
            else:
                break
        new_idf_fields = [i for j, i in enumerate(original_idf_fields) if j not in indeces_to_remove]
        new_branch_object = IDFObject([core_object.object_name] + new_idf_fields)
        # return a list since some transitions may split/add new objects
        return TransitionReturn([new_branch_object])
