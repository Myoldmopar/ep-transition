from eptransition.rules.rules85to86 import branch as branch86
from eptransition.rules.rules86to87 import controller_list, branch as branch87, output_variables as output87


class TypeEnum(object):
    IDF = "idf"
    JSON = "json"


class VersionInformation(object):
    def __init__(self, version_float, file_type, transitions, outputs):
        self.version = version_float
        self.file_type = file_type
        self.transitions = transitions
        self.output_variable_transition = outputs


# We need to have the very first baseline in here even if it isn't ever a target transition
Version85 = VersionInformation(8.5, TypeEnum.IDF,
                               transitions=[],
                               outputs=None)
Version86 = VersionInformation(8.6, TypeEnum.IDF,
                               transitions=[
                                   branch86.BranchTransitionRule
                               ],
                               outputs=None)
Version87 = VersionInformation(8.7, TypeEnum.IDF,
                               transitions=[
                                   branch87.BranchTransitionRule,
                                   controller_list.ControllerListTransitionRule,
                               ],
                               outputs=output87.OutputVariableTransitionRule)

VERSIONS = {'8.5': Version85, '8.6': Version86, '8.7': Version87}
