class IDDField:
    def __init__(self, an_index):
        self.field_an_index = an_index
        self.meta_data = {}
        self.field_name = None
        self.field_index = None


class IDDObject:
    def __init__(self, name):
        self.name = name
        self.meta_data = {}
        self.fields = []


class IDDGroup:
    def __init__(self, name):
        self.name = name
        self.objects = []


class IDDStructure:
    def __init__(self, file_path):
        self.file_path = file_path
        # TODO: Parse and store IDD version
        self.version = None
        self.single_line_objects = []
        self.groups = []

    def get_object_by_type(self, type_to_get):
        # check the normal objects
        for g in self.groups:
            for o in g.objects:
                if o.name.upper() == type_to_get.upper():
                    return o
        # check single line objects? Weird...but might be useful
        for o in self.single_line_objects:
            if o.upper() == type_to_get.upper():
                return o
        # if we haven't returned, fail
        return None
