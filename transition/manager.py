import version
from filetype import TypeEnum


class TransitionFile(object):
    def __init__(self, input_file):
        self.input_file = input_file
        if version.START_VERSION.file_type == TypeEnum.IDF:
            pass  # read as IDF
            # eventually we'll just infer the file types for in/out and act accordingly
