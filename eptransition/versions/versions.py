from eptransition.rules.base_rule import TransitionRule, OutputVariableTransitionRule
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


class SingleTransition(object):
    """
    Internal init only version information class

    :param float start_version: The major.minor floating point version identifier for the start version of this
                                transition
    :param float end_version: The major.minor floating point version identifier for the end version of this transition
    :param [TransitionRule] transitions: A list of class names that derive from TransitionRule as implemented for this
                                         version
    :param OutputVariableTransitionRule_or_None outputs: Name of a class that derives from OutputVariableTransitionRule, as
                                                 implemented for this version
    """
    def __init__(self, start_version, end_version, transitions, outputs):
        # error handling first
        try:
            start_version = float(start_version)
        except:  # pragma no cover
            raise Exception()
        try:
            end_version = float(end_version)
        except:  # pragma no cover
            raise Exception()
        if not all([issubclass(x, TransitionRule) for x in transitions]):  # pragma no cover
            raise Exception()
        if outputs is not None:
            if not issubclass(outputs, OutputVariableTransitionRule):  # pragma no cover
                raise Exception()
        # then assign class variables
        self.start_version = start_version
        self.end_version = end_version
        self.transitions = transitions
        self.output_variable_transition = outputs


# We need to have the very first baseline in here even if it isn't ever a target transition
Transition84_85 = SingleTransition(8.4, 8.5,
                                   transitions=[],
                                   outputs=None)
Transition85_86 = SingleTransition(8.5, 8.6,
                                   transitions=[
                                       branch86.Rule,
                                       inletmixer86.Rule,
                                       supplymixer86.Rule,
                                       otherequipment86.Rule,
                                       zonehvac_adu86.Rule
                                   ],
                                   outputs=None)
Transition86_87 = SingleTransition(8.6, 8.7,
                                   transitions=[
                                       branch87.Rule,
                                       controller_list87.Rule,
                                   ],
                                   outputs=output87.Rule)

FILE_TYPES = {8.4: TypeEnum.IDF, 8.5: TypeEnum.IDF, 8.6: TypeEnum.IDF, 8.7: TypeEnum.IDF}
TRANSITIONS = {8.4: Transition84_85, 8.5: Transition85_86, 8.6: Transition86_87}  # key is start version
