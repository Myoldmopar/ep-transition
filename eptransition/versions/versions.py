from eptransition.rules.rules85to86 import (
    branch as branch86,
    airterminal_singleduct_inletsidemixer as inletmixer86,
    airterminal_singleduct_supplysidemixer as supplymixer86,
    otherequipment as otherequipment86,
    zonehvac_airdistributionunit as zonehvac_adu86
)
from eptransition.rules.rules86to87 import (
    controller_list as controller_list87,
    branch as branch87,
    output_variables as output87
)


class TypeEnum(object):
    """
    Simple enumeration style class laying out the possible file types available
    """
    IDF = "idf"
    JSON = "json"


class VersionInformation(object):
    """
    Internal init only version information class

    :param float version_float: The major.minor floating point version identifier for this version
    :param str file_type: The file type for this version, from the TypeEnum class
    :param [TransitionRule] transitions: A list of class names that derive from TransitionRule as implemented for this
                                         version
    :param OutputVariableTransitionRule outputs: Name of a class that derives from OutputVariableTransitionRule, as
                                                 implemented for this version
    """
    def __init__(self, version_float, file_type, transitions, outputs):
        self.version = version_float
        self.file_type = file_type
        # TODO: Validate all transitions derive from TransitionRule
        self.transitions = transitions
        # TODO: Validate output transition derives from OutputVariableTransitionRule
        self.output_variable_transition = outputs


# We need to have the very first baseline in here even if it isn't ever a target transition
Version85 = VersionInformation(8.5, TypeEnum.IDF,
                               transitions=[],
                               outputs=None)
Version86 = VersionInformation(8.6, TypeEnum.IDF,
                               transitions=[
                                   branch86.Rule,
                                   inletmixer86.Rule,
                                   supplymixer86.Rule,
                                   otherequipment86.Rule,
                                   zonehvac_adu86.Rule
                               ],
                               outputs=None)
Version87 = VersionInformation(8.7, TypeEnum.IDF,
                               transitions=[
                                   branch87.Rule,
                                   controller_list87.Rule,
                               ],
                               outputs=output87.Rule)

VERSIONS = {'8.5': Version85, '8.6': Version86, '8.7': Version87}
