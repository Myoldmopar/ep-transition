class UnimplementedMethodException(Exception):
    """
    This exception occurs when a call is made to a function that should be implemented in a derived class
    but isn't, so the base class function is called.  This is a developer issue.
    """
    pass


class MalformedIDFException(Exception):
    """
    This exception occurs when an invalid syntax is detected when processing an IDF.  This is likely a problem
    with the idf itself.
    """
    pass


class FileAccessException(Exception):
    """
    This exception occurs when the transition tool encounters a problem accessing a prescribed input or output file.
    """
    pass


class FileTypeException(Exception):
    """
    This exception occurs when the prescribed file types do not match the expected conditions.
    """
    pass


class ManagerProcessingException(Exception):
    """
    This exception occurs when the transition tool encounters an unexpected issue when doing the transition.
    """
    def __init__(self, msg, issues=None):
        self.message = msg
        self.issues = issues

    def __str__(self):
        msg = ''
        if self.issues:
            for i in self.issues:
                msg += str(i) + '\n'
        msg += self.message
        return msg


class ProcessingException(Exception):
    """
    This exception occurs when an unexpected error occurs during the processing of an input file.
    """
    def __init__(self, message, line_index=None, object_name='', field_name=''):
        super(ProcessingException, self).__init__(message)
        self.line_index = line_index

    def __str__(self):
        return "Processing Exception on line number " + str(self.line_index)  # pragma: no cover
