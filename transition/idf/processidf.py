from idfobject import IDFObject
from .. import inputprocessor


class IDFProcessor(inputprocessor.InputFileProcessor):

    def process_one_file(self, opened_file_object):
        # phase 0: read in lines of file
        lines = opened_file_object.readlines()

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
                    lines_a.append(this_line)

        # intermediates: join entire array and re-split by semicolon
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