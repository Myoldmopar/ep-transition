class IDFObject(object):
    def __init__(self, tokens):
        self.object_name = tokens[0]
        self.fields = tokens[1:]

    def object_string(self):
        if len(self.fields) == 0:
            s = self.object_name + ";\n"
        else:
            s = self.object_name + ",\n"
            padding_size = 25
            for field in self.fields[:-1]:
                s += "  " + (field + ',').ljust(padding_size) + "!-\n"
            s += "  " + (self.fields[-1] + ';').ljust(padding_size) + "!-\n"
        return s

    def write_object(self, file_object):
        file_object.write(self.object_string())
