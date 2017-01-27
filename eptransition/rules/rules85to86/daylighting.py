from eptransition.idf.objects import IDFObject
from eptransition.rules.base_rule import TransitionRule, TransitionReturn
from eptransition.rules.rules85to86.utilities import build_ref_pt_list


class Rule(TransitionRule):  # pragma no cover

    def get_name_of_object_to_transition(self):
        return "DAYLIGHTING:CONTROLS"

    def get_names_of_dependent_objects(self):
        return ["DAYLIGHTING:DELIGHT:CONTROLS", "DAYLIGHTING:DELIGHT:REFERENCEPOINT"]

    def transition(self, core_object, dependent_objects):  # pragma no cover
        original_idf_fields = core_object.fields
        new_idf_fields = list()
        new_idf_fields.append(original_idf_fields[0] + "_DaylCtrl")  # 0
        new_idf_fields.append(original_idf_fields[0])  # 1
        new_idf_fields.append("SplitFlux")  # 2
        try:
            new_idf_fields.append(original_idf_fields[19])  # 3
        except IndexError:
            new_idf_fields.append("")
        if original_idf_fields[12] == "1":
            new_idf_fields.append("Continuous")  # 4
        elif original_idf_fields[12] == "2":
            new_idf_fields.append("Stepped")  # 4
        elif original_idf_fields[12] == "3":
            new_idf_fields.append("ContinuousOff")  # 4
        else:
            new_idf_fields.append("Continuous")  # 4
        new_idf_fields.append(original_idf_fields[15])  # 5
        new_idf_fields.append(original_idf_fields[16])  # 6
        if original_idf_fields[17] == "0":
            new_idf_fields.append("")  # 7
        else:
            new_idf_fields.append(original_idf_fields[17])  # 7
        new_idf_fields.append(original_idf_fields[18])  # 8
        new_idf_fields.append(original_idf_fields[0] + "_DaylRefPt1")  # 9
        new_idf_fields.append(original_idf_fields[13])  # 10
        new_idf_fields.append(original_idf_fields[14])  # 11
        new_idf_fields.append("")  # 12
        new_idf_fields.append(original_idf_fields[0] + "_DaylRefPt1")  # 13
        new_idf_fields.append(original_idf_fields[8])  # 14
        new_idf_fields.append(original_idf_fields[10])  # 15
        if original_idf_fields[1] == "2":
            new_idf_fields.append(original_idf_fields[0] + "_DaylRefPt2")  # 16
            new_idf_fields.append(original_idf_fields[9])  # 17
            new_idf_fields.append(original_idf_fields[11])  # 18
        new_control_object = IDFObject([core_object.object_name] + new_idf_fields)
        objects_to_write = [new_control_object]

        ref_pt_fields = list()
        ref_pt_fields.append("Daylighting:ReferencePoint")
        ref_pt_fields.append(original_idf_fields[0] + "_DaylRefPt1")
        ref_pt_fields.append(original_idf_fields[0])
        ref_pt_fields.append(original_idf_fields[2])
        ref_pt_fields.append(original_idf_fields[3])
        ref_pt_fields.append(original_idf_fields[4])
        ref_pt_object_1 = IDFObject(ref_pt_fields)
        objects_to_write.append(ref_pt_object_1)

        if original_idf_fields[1] == "2":
            ref_pt_fields = list()
            ref_pt_fields.append("Daylighting:ReferencePoint")
            ref_pt_fields.append(original_idf_fields[0] + "_DaylRefPt2")
            ref_pt_fields.append(original_idf_fields[0])
            ref_pt_fields.append(original_idf_fields[5])
            ref_pt_fields.append(original_idf_fields[6])
            ref_pt_fields.append(original_idf_fields[7])
            ref_pt_object_1 = IDFObject(ref_pt_fields)
            objects_to_write.append(ref_pt_object_1)

        return TransitionReturn(objects_to_write)


class Rule2(TransitionRule):  # pragma no cover

    def get_name_of_object_to_transition(self):
        return "DAYLIGHTING:DELIGHT:CONTROLS"

    def get_names_of_dependent_objects(self):
        return ["DAYLIGHTING:DELIGHT:REFERENCEPOINT", "DAYLIGHTING:DELIGHT:CONTROLS"]

    def transition(self, core_object, dependent_objects):  # pragma no cover
        daylight_ref_pts = build_ref_pt_list(dependent_objects["DAYLIGHTING:DELIGHT:REFERENCEPOINT"],
                                             dependent_objects["DAYLIGHTING:DELIGHT:CONTROLS"])
        original_idf_fields = core_object.fields
        new_idf_fields = list()
        new_idf_fields.append("Daylighting:Controls")
        new_idf_fields.append(original_idf_fields[0])  # 0
        new_idf_fields.append(original_idf_fields[1])  # 1
        new_idf_fields.append("DElight")  # 2
        new_idf_fields.append("")  # 3
        if original_idf_fields[4] == "1":
            new_idf_fields.append("Continuous")  # 4
        elif original_idf_fields[4] == "2":
            new_idf_fields.append("Stepped")  # 4
        elif original_idf_fields[4] == "3":
            new_idf_fields.append("ContinuousOff")  # 4
        else:
            new_idf_fields.append("Continuous")  # 4
        new_idf_fields.append(original_idf_fields[3])  # 5
        new_idf_fields.append(original_idf_fields[4])  # 6
        if original_idf_fields[5] == "0":
            new_idf_fields.append("")  # 7
        else:
            new_idf_fields.append(original_idf_fields[5])  # 7
        new_idf_fields.append(original_idf_fields[6])  # 8
        new_idf_fields.append("")  # 9
        new_idf_fields.append("0")  # 10
        new_idf_fields.append("")  # 11
        new_idf_fields.append(original_idf_fields[7])  # 12
        for ref_pt in daylight_ref_pts:
            if ref_pt.control_name.upper() == original_idf_fields[0].upper():
                new_idf_fields.append(ref_pt.ref_pt_name)
                new_idf_fields.append(ref_pt.frac_zone)
                new_idf_fields.append(ref_pt.illum_set_pt)
        return TransitionReturn([IDFObject(new_idf_fields)])


class Rule3(TransitionRule):  # pragma no cover

    def get_name_of_object_to_transition(self):
        return "DAYLIGHTING:DELIGHT:REFERENCEPOINT"

    def get_names_of_dependent_objects(self):
        return ["DAYLIGHTING:DELIGHT:REFERENCEPOINT", "DAYLIGHTING:DELIGHT:CONTROLS"]

    def transition(self, core_object, dependent_objects):  # pragma no cover
        daylight_ref_pts = build_ref_pt_list(dependent_objects["DAYLIGHTING:DELIGHT:REFERENCEPOINT"],
                                             dependent_objects["DAYLIGHTING:DELIGHT:CONTROLS"])
        original_idf_fields = core_object.fields
        new_idf_fields = list()
        new_idf_fields.append("Daylighting:ReferencePoint")
        new_idf_fields.append(original_idf_fields[0])  # 0
        for ref_pt in daylight_ref_pts:
            if ref_pt.control_name.upper() == original_idf_fields[1].upper():
                new_idf_fields.append(ref_pt.zone_name)
                break
        new_idf_fields.append(original_idf_fields[2])
        new_idf_fields.append(original_idf_fields[3])
        new_idf_fields.append(original_idf_fields[4])
        return TransitionReturn([IDFObject(new_idf_fields)])
