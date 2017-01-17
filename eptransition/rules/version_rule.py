from eptransition.idf.objects import IDFObject
from eptransition.rules import base_rule


class VersionRule(base_rule.TransitionRule):
    """
    This class implements, in a generic fashion, the transition rule for the Version object.  By passing in the
    identifier for the target version, the rules are set up so this doesn't have to change for each version.

    :param end_version: The new value for the version object's single field: Version ID
    """
    def __init__(self, end_version):
        base_rule.TransitionRule.__init__(self)
        self.end_version_id = end_version

    def get_name_of_object_to_transition(self):
        return "Version"

    def get_names_of_dependent_objects(self):
        return []

    def transition(self, core_object, dependent_objects):
        new_idf_fields = [self.end_version_id]
        new_version_object = IDFObject([core_object.object_name] + new_idf_fields)
        return base_rule.TransitionReturn([new_version_object])
