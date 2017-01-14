from filetype import TypeEnum


class VersionInformation(object):
    def __init__(self, version_float, file_type):
        self.version = version_float
        self.file_type = file_type


# TODO: This should be a start/end for a specific version
START_VERSION = VersionInformation(8.6, TypeEnum.IDF)
END_VERSION = VersionInformation(8.7, TypeEnum.IDF)
