class RefPtStructure:  # pragma no cover

    def __init__(self, ref_pt_name, control_name, x, y, z, frac_zone, illum_set_pt, zone_name):
        self.ref_pt_name = ref_pt_name
        self.control_name = control_name
        self.x = x
        self.y = y
        self.z = z
        self.frac_zone = frac_zone
        self.illum_set_pt = illum_set_pt
        self.zone_name = zone_name


def build_ref_pt_list(ref_pt_object_list, control_object_list):  # pragma no cover

    my_ref_pt_structures = []
    for ref_pt in ref_pt_object_list:
        this_ref_pt_name = ref_pt.fields[0]
        this_control_name = ref_pt.fields[0]
        this_x = ref_pt.fields[0]
        this_y = ref_pt.fields[0]
        this_z = ref_pt.fields[0]
        this_frac_zone = ref_pt.fields[0]
        this_illum_set_pt = ref_pt.fields[0]
        this_zone_name = ''
        for control_object in control_object_list:
            if this_ref_pt_name.upper() == control_object.fields[0].upper():
                this_zone_name = control_object.fields[1]
                break
        my_ref_pt_structures.append(RefPtStructure(this_ref_pt_name, this_control_name, this_x, this_y, this_z,
                                                   this_frac_zone, this_illum_set_pt, this_zone_name))
    return my_ref_pt_structures
