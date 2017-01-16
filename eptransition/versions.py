from eptransition.rules.rules85to86 import branch as branch86
from eptransition.rules.rules86to87 import controller_list, branch as branch87


class TypeEnum(object):
    IDF = "idf"
    JSON = "json"


class VersionInformation(object):
    def __init__(self, version_float, file_type, transitions_to_do):
        self.version = version_float
        self.file_type = file_type
        self.transitions = transitions_to_do


# We need to have the very first baseline in here even if it isn't ever a target transition
Version85 = VersionInformation(8.5, TypeEnum.IDF, [])
Version86 = VersionInformation(8.6, TypeEnum.IDF, [branch86.BranchTransitionRule])
Version87 = VersionInformation(8.7, TypeEnum.IDF, [
    branch87.BranchTransitionRule, controller_list.ControllerListTransitionRule])

VERSIONS = {'8.5': Version85, '8.6': Version86, '8.7': Version87}
