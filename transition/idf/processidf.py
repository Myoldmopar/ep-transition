import os

from idfobject import IDFObject
from .. import exceptions
from .. import inputprocessor


class IDFProcessor(inputprocessor.InputFileProcessor):
    def __init__(self):
        self.input_file_stream = None

    def process_file_given_file_path(self, file_path):
        if not os.path.exists(file_path):
            raise exceptions.ProcessingException("Input file not found=\"" + file_path + "\"")
        self.input_file_stream = open(file_path, 'r')
        return self.process_file()

    def process_file_via_stream(self, input_file_stream):
        self.input_file_stream = input_file_stream
        return self.process_file()

    def process_file(self):
        # phase 0: read in lines of file
        lines = self.input_file_stream.readlines()

        # phases 1 and 2: remove comments and blank lines
        lines_a = []
        for line in lines:
            line_text = line.strip()
            this_line = ""
            if len(line_text) > 0:
                exclamation = line_text.find("!")
                if exclamation == -1:
                    this_line = line_text
                elif exclamation == 0:
                    this_line = ""
                elif exclamation > 0:
                    this_line = line_text[:exclamation]
                if not this_line == "":
                    lines_a.append(this_line.strip())

        # intermediate: check for malformed idf syntax
        for l in lines_a:
            if not (l.endswith(',') or l.endswith(';')):
                raise exceptions.MalformedIDFException("IDF line doesn't end with comma/semicolon\nline:\"" + l + "\"")

        # intermediate: join entire array and re-split by semicolon
        idf_data_joined = ''.join(lines_a)
        idf_object_strings = idf_data_joined.split(";")

        # phase 3: inspect each object and its fields
        object_details = []
        idf_objects = []
        for obj in idf_object_strings:
            tokens = obj.split(",")
            nice_object = [t.strip() for t in tokens]
            if len(nice_object) == 1:
                if nice_object[0] == "":
                    continue
            object_details.append(nice_object)
            idf_objects.append(IDFObject(nice_object))

        return idf_objects
