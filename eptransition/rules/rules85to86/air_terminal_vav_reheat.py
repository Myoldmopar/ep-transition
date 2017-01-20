from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn


class Rule(TransitionRule):
    def get_name_of_object_to_transition(self):
        return "AirTerminal:SingleDuct:VAV:Reheat"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):  # pragma no cover
        # If F16 is "Reverse" and both F17 and F18 (N7 and N8) are blank, do nothing.
        # If F16 is "reverse" and either F17 or F18 is not blank, replace "Reverse" with" ReverseWithLimits".
        original_idf_fields = core_object.fields
        original_f16 = original_idf_fields[15]
        original_f17 = original_idf_fields[16]
        original_f18 = original_idf_fields[17]
        new_idf_fields = original_idf_fields

        if original_f16.upper() == "REVERSE":
            if original_f17 == "" and original_f18 == "":
                # do nothing
                pass
            else:
                new_idf_fields[15] = "ReverseWithLimits"
        new_terminal_object = IDFObject([core_object.object_name] + new_idf_fields)
        return TransitionReturn([new_terminal_object])
