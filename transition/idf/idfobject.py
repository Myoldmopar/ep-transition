class ValidationIssue:
    def __init__(self, object_name, field_name=None, message=None):
        self.object_name = object_name
        self.field_name = field_name
        self.message = message


class IDFObject(object):
    def __init__(self, tokens):
        self.object_name = tokens[0]
        self.fields = tokens[1:]

    def object_string(self, idd_object=None):
        # TODO: Add units in {} to all numeric fields, not sure about determining dimensionless
        if not idd_object:
            idd_fields = [''] * len(self.fields)
        else:
            idd_fields = []
            for field in idd_object.fields:
                idd_fields.append(field.field_name)
        if len(self.fields) == 0:
            s = self.object_name + ";\n"
        else:
            s = self.object_name + ",\n"
            padding_size = 25
            last_idd_field = idd_fields[len(self.fields) - 1]
            for idf_field, idd_field in zip(self.fields[:-1], idd_fields):
                s += "  " + (idf_field + ',').ljust(padding_size) + "!- " + idd_field + "\n"
            s += "  " + (self.fields[-1] + ';').ljust(padding_size) + "!- " + last_idd_field + "\n"
        return s

    def validate(self, idd_object):
        issues = []
        # need to first check min-fields
        # need to check \default for each field to fill it first if it is blank
        # need to check \type choice and \keys
        for idf, idd in zip(self.fields, idd_object.fields):
            if '\\required-field' in idd.meta_data:
                if idf == '':
                    issues.append(ValidationIssue(idd_object.name, idd.field_name,
                                                  'Blank required field found'))
                    continue
            an_code = idd.field_an_index
            if an_code[0] == 'N':
                try:
                    number = float(idf)
                    if '\\maximum' in idd.meta_data:
                        max_constraint_string = idd.meta_data['\\maximum'][0]
                        if max_constraint_string[0] == "<":
                            max_val = float(max_constraint_string[1:])
                            if number >= max_val:
                                issues.append(ValidationIssue(
                                    idd_object.name, idd.field_name,
                                    'Field value higher than idd-specified maximum>; actual={}, max={}'.format(
                                        number, max_val)))
                        else:
                            max_val = float(max_constraint_string)
                            if number > max_val:
                                issues.append(ValidationIssue(
                                    idd_object.name, idd.field_name,
                                    'Field value higher than idd-specified maximum; actual={}, max={}'.format(
                                        number, max_val)))
                    if '\\minimum' in idd.meta_data:
                        min_constraint_string = idd.meta_data['\\minimum'][0]
                        if min_constraint_string[0] == ">":
                            min_val = float(min_constraint_string[1:])
                            if number <= min_val:
                                issues.append(ValidationIssue(
                                    idd_object.name, idd.field_name,
                                    'Field value lower than idd-specified minimum<; actual={}, max={}'.format(
                                        number, max_val)))
                        else:
                            min_val = float(min_constraint_string)
                            if number < min_val:
                                issues.append(ValidationIssue(
                                    idd_object.name, idd.field_name,
                                    'Field value lower than idd-specified minimum; actual={}, max={}'.format(
                                        number, max_val)))
                except ValueError:
                    if '\\autosizable' in idd.meta_data and idf.upper() == 'AUTOSIZE':
                        pass  # everything is ok
                    elif idf.upper() == 'AUTOSIZE':
                        issues.append(ValidationIssue(idd_object.name, idd.field_name,
                                      'Autosize detected in numeric field that is _not_ listed autosizable'))
                    else:
                        issues.append(ValidationIssue(idd_object.name, idd.field_name,
                                                      'Non-numeric value in idd-specified numeric field'))
        return issues

    def write_object(self, file_object):
        file_object.write(self.object_string())


class IDFStructure(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.version = None
        self.objects = None

    def get_idf_objects_by_type(self, type_to_get):
        return [i for i in self.objects if i.object_name.upper() == type_to_get.upper()]

    def write_idf(self, idd_structure):
        with open('/tmp/new_idf', 'w') as f:
            for idf_obj in self.objects:
                idd_obj = idd_structure.get_object_by_type(idf_obj.object_name)
                f.write(idf_obj.object_string(idd_obj) + '\n')
