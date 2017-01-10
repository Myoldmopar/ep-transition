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
        self.s_version = None
        self.single_line_objects = []
        self.groups = []
