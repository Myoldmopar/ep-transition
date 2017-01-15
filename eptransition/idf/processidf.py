import StringIO
import os

from eptransition import epexceptions
from eptransition.idf.idfobject import IDFObject, IDFStructure


class IDFProcessor:
    def __init__(self):
        self.idf = None
        self.file_path = None
        self.input_file_stream = None

    def process_file_given_file_path(self, file_path):
        if not os.path.exists(file_path):
            raise epexceptions.ProcessingException("Input file not found=\"" + file_path + "\"")
        self.input_file_stream = open(file_path, 'r')
        self.file_path = file_path
        return self.process_file()

    def process_file_via_stream(self, input_file_stream):
        self.input_file_stream = input_file_stream
        self.file_path = "/streamed/idf"
        return self.process_file()

    def process_file_via_string(self, idf_string):
        self.input_file_stream = StringIO.StringIO(idf_string)
        self.file_path = "/string/idf/snippet"
        return self.process_file()

    def process_file(self):
        self.idf = IDFStructure(self.file_path)
        # phase 0: read in lines of file
        lines = self.input_file_stream.readlines()

        class Blob:
            COMMENT = 1
            OBJECT = 2

            def __init__(self, blob_type, blob_lines=None):
                self.blob_type = blob_type
                if blob_lines is None:
                    blob_lines = []
                self.lines = blob_lines

        # so let's try keeping the idf in blobs of either comment data or object data
        current_blob = None
        initial_blobs = []
        for line in lines:
            line_text = line.strip()
            if len(line_text) == 0:
                continue
            elif line_text.startswith('!'):
                if current_blob is None:
                    current_blob = Blob(Blob.COMMENT)
                elif current_blob.blob_type == Blob.OBJECT:
                    initial_blobs.append(current_blob)
                    current_blob = Blob(Blob.COMMENT)
                current_blob.lines.append(line_text)
            else:
                if current_blob is None:
                    current_blob = Blob(Blob.OBJECT)
                elif current_blob.blob_type == Blob.COMMENT:
                    initial_blobs.append(current_blob)
                    current_blob = Blob(Blob.OBJECT)
                current_blob.lines.append(line_text)
        if current_blob is not None:
            initial_blobs.append(current_blob)

        # next let's go blob by blob and clean up any trailing comments and such
        idf_objects = []
        for initial_blob in initial_blobs:
            if initial_blob.blob_type == Blob.COMMENT:
                idf_objects.append(IDFObject(initial_blob.lines, True))
            else:
                out_lines = []
                for line in initial_blob.lines:
                    line_text = line.strip()
                    this_line = ""
                    if len(line_text) > 0:
                        exclamation = line_text.find("!")
                        if exclamation == -1:
                            this_line = line_text
                        elif exclamation > 0:
                            this_line = line_text[:exclamation]
                        if not this_line == "":
                            out_lines.append(this_line.strip())
                # check these object lines for malformed idf syntax
                for l in out_lines:
                    if not (l.endswith(',') or l.endswith(';')):
                        raise epexceptions.MalformedIDFException(
                            "IDF line doesn't end with comma/semicolon\nline:\"" + l + "\"")
                # the last line in an idf object blob should have a semicolon; if it doesn't it might indicate
                # a comment block in the middle of a single idf object
                if not out_lines[-1].endswith(';'):
                    raise epexceptions.MalformedIDFException(
                        "Encountered a missing semicolon condition; this can indicate comments placed within" +
                        " a single idf object.  This is valid IDF for EnergyPlus, but this translator does not yet" +
                        " handle such condition."
                    )
                # intermediate: join entire array and re-split by semicolon
                idf_data_joined = ''.join(out_lines)
                idf_object_strings = idf_data_joined.split(";")
                # phase 3: inspect each object and its fields
                for obj in idf_object_strings:
                    tokens = obj.split(",")
                    nice_object = [t.strip() for t in tokens]
                    if len(nice_object) == 1:
                        if nice_object[0] == "":
                            continue
                    idf_objects.append(IDFObject(nice_object))

        self.idf.objects = idf_objects
        return self.idf
