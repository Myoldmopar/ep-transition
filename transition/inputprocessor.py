from exceptions import UnimplementedMethodException


class InputFileProcessor(object):
    def process_a_file(self, opened_file_object):
        """
        Abstract declaration of file processor, should return a list of IDFObject instances
        :param opened_file_object: already opened file-type object to read from
        :return:
        """
        raise UnimplementedMethodException("Derived classes of InputFileProcessor must override \"process_a_file\"")
