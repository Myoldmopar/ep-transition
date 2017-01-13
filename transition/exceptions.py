class UnimplementedMethodException(Exception):
    pass


class MalformedIDFException(Exception):
    pass


class ProcessingException(Exception):
    def __init__(self, message, line_index=None, object_name='', field_name=''):
        super(ProcessingException, self).__init__(message)
        self.line_index = line_index

    def __str__(self):
        print("Processing Exception on line number " + str(self.line_index))  # pragma: no cover
