from eptransition.rules.rules86to87 import controller_list, branch


class TypeEnum(object):
    IDF = "idf"
    JSON = "json"


class VersionInformation(object):
    def __init__(self, version_float, file_type, transitions_to_do):
        self.version = version_float
        self.file_type = file_type
        self.transitions = transitions_to_do


Version86 = VersionInformation(8.6, TypeEnum.IDF, [])
Version87 = VersionInformation(8.7, TypeEnum.IDF, [
    branch.BranchTransitionRule, controller_list.ControllerListTransitionRule])

VERSIONS = {'8.6': Version86, '8.7': Version87}
