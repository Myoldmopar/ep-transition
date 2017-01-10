class IDFObject(object):
    def __init__(self, tokens):
        self.object_name = tokens[0]
        self.fields = tokens[1:]

    def object_string(self, idd_object=None):
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

    def write_object(self, file_object):
        file_object.write(self.object_string())
