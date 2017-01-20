from eptransition.exceptions import ManagerProcessingException
from eptransition.rules.base_rule import TransitionRule, OutputVariableTransitionRule
from eptransition.rules.templates.remove_single_field import Rule as remove_field

from eptransition.rules.rules85to86.branch import Rule as branch86
from eptransition.rules.rules85to86.airterminal_singleduct_inletsidemixer import Rule as inletmixer86
from eptransition.rules.rules85to86.airterminal_singleduct_supplysidemixer import Rule as supplymixer86
from eptransition.rules.rules85to86.otherequipment import Rule as otherequipment86
from eptransition.rules.rules85to86.zonehvac_airdistributionunit import Rule as zonehvac_adu86
from eptransition.rules.rules85to86.empd import Rule as empd86
from eptransition.rules.rules85to86.coilheatinggas import Rule as coilheatinggas86
from eptransition.rules.rules85to86.exteriorfuelequipment import Rule as exteriorequip86
from eptransition.rules.rules85to86.chillerheater import Rule as chillerheater86
from eptransition.rules.rules85to86.setpoint_managers import Rule as setpointmanagers86a
from eptransition.rules.rules85to86.setpoint_managers import Rule2 as setpointmanagers86b
from eptransition.rules.rules85to86.ems_actuator import Rule as actuator86
from eptransition.rules.rules85to86.air_terminal_vav_reheat import Rule as vavreheat86

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
    Internal version information class

    :param float start_version: The major.minor floating point version identifier for the start version of this
                                transition
    :param float end_version: The major.minor floating point version identifier for the end version of this transition
    :param [TransitionRule] transitions: A list of class names that derive from TransitionRule as implemented for this
                                         version
    :param OutputVariableTransitionRule_or_None outputs: Name of a class that derives from OutputVariableTransitionRule,
                                                         as implemented for this version
    :raises ManagerProcessingException: for any invalid inputs
    """

    def __init__(self, start_version, end_version, transitions, outputs):
        # error handling first
        try:
            start_version = float(start_version)
        except ValueError:
            raise ManagerProcessingException("Error in SingleTransition construction; non-float start version")
        try:
            end_version = float(end_version)
        except ValueError:
            raise ManagerProcessingException("Error in SingleTransition construction; non-float end version")
        if not all([isinstance(x, TransitionRule) for x in transitions]):
            raise ManagerProcessingException("Error in SingleTransition construction; all transition rules must " +
                                             "derive from TransitionRule")
        if outputs is not None:
            if not isinstance(outputs, OutputVariableTransitionRule):
                raise ManagerProcessingException("Error in SingleTransition construction; output transition must " +
                                                 "derive from OutputVariableTransitionRule")
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
                                       branch86(),
                                       inletmixer86(),
                                       supplymixer86(),
                                       otherequipment86(),
                                       zonehvac_adu86(),
                                       empd86(),
                                       coilheatinggas86(),
                                       exteriorequip86(),
                                       chillerheater86(),
                                       setpointmanagers86a(),
                                       setpointmanagers86b(),
                                       actuator86(),
                                       vavreheat86(),
                                       remove_field("HVACTemplate:System:UnitarySystem", 56),  # dehumidification
                                       remove_field("HVACTemplate:System:Unitary", 39),  # dehumidification
                                   ],
                                   outputs=None)
Transition86_87 = SingleTransition(8.6, 8.7,
                                   transitions=[
                                       branch87.Rule(),
                                       controller_list87.Rule(),
                                   ],
                                   outputs=output87.Rule())

FILE_TYPES = {8.4: TypeEnum.IDF, 8.5: TypeEnum.IDF, 8.6: TypeEnum.IDF, 8.7: TypeEnum.IDF}
TRANSITIONS = {8.4: Transition84_85, 8.5: Transition85_86, 8.6: Transition86_87}  # key is start version
