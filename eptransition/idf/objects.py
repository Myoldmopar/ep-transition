class ValidationIssue:
    """
    This init only class stores information about any issue that occurred when reading an IDF file.

    :param str object_name: The object type that was being validated when this issue arose
    :param str field_name: The field name that was being validated when this issue arose, if available.
    :param str message: A descriptive message for this issue
    """
    def __init__(self, object_name, field_name=None, message=None):
        self.object_name = object_name
        self.field_name = field_name
        self.message = message

    def __str__(self):  # pragma no cover
        return "Issue found: object {}; field {}; message: {}".format(self.object_name, self.field_name, self.message)


class IDFObject(object):
    """
    This class defines a single IDF object.  An IDF object is either a comma/semicolon delimited list of actual
    object data, or a block of line delimited comments.  Blocks of comment lines are treated as IDF objects so they can
    be intelligently written back out to a new IDF file after transition in the same-ish location.

    Relevant members are listed here:

    :ivar str object_name: IDD Type, or name, of this object
    :ivar [str] fields: A list of strings, one per field, found for this object in the IDF file

    Constructor parameters:

    :param [str] tokens: A list of tokens defining this idf object, the first token in the list is the object type.
    :param bool comment_blob: A signal that this list is comment data, and not an actual IDF object; default is False.
                              indicating it is meaningful IDF data.
    """
    def __init__(self, tokens, comment_blob=False):
        self.comment = comment_blob
        if comment_blob:
            self.object_name = "COMMENT"
            self.fields = tokens
        else:
            self.object_name = tokens[0]
            self.fields = tokens[1:]

    def object_string(self, idd_object=None):
        """
        This function creates an intelligently formed IDF object.  If the current instance is comment data, it simply
        writes the comment block out, line delimited, otherwise it writes out proper IDF syntax.  If the matching IDD
        object is passed in as an argument, the field names are matched from that to create a properly commented
        IDF object.

        :param IDDObject idd_object: The IDDObject structure that matches this IDFObject
        :return: A string representation of the IDF object or comment block
        """
        s = ''
        if self.comment:
            for comment_line in self.fields:
                s += comment_line + '\n'
            return s
        if not idd_object:
            if len(self.fields) == 0:
                s = self.object_name + ";\n"
            else:
                s = self.object_name + ",\n"
                padding_size = 25
                for index, idf_field in enumerate(self.fields):
                    if index == len(self.fields) - 1:
                        terminator = ';'
                    else:
                        terminator = ','
                    s += "  " + (idf_field + terminator).ljust(
                        padding_size) + "!- \n"
            return s
        else:
            if len(self.fields) == 0:
                s = self.object_name + ";\n"
            else:
                idd_fields = idd_object.fields
                s = self.object_name + ",\n"
                padding_size = 25
                for index, idf_idd_fields in enumerate(zip(self.fields, idd_fields)):
                    idf_field, idd_field = idf_idd_fields
                    if index == len(self.fields) - 1:
                        terminator = ';'
                    else:
                        terminator = ','
                    if '\\units' in idd_field.meta_data:
                        units_string = ' {' + idd_field.meta_data['\\units'][0] + '}'
                    else:
                        units_string = ''
                    s += "  " + (str(idf_field) + terminator).ljust(
                        padding_size) + "!- " + idd_field.field_name + units_string + "\n"
            return s

    def validate(self, idd_object):
        """
        This function validates the current IDF object instance against standard IDD field tags such as minimum and
        maximum, etc.

        :param IDDObject idd_object: The IDDObject structure that matches this IDFObject
        :return: A list of ValidationIssue instances, each describing an issue encountered
        """
        issues = []
        # TODO: first check min-fields
        # TODO: check \default for each field to fill it first if it is blank
        # TODO: check \type choice and \keys
        for idf, idd in zip(self.fields, idd_object.fields):
            if '\\required-field' in idd.meta_data:
                if idf == '':
                    issues.append(ValidationIssue(idd_object.name, idd.field_name,
                                                  'Blank required field found'))
                    continue
            an_code = idd.field_an_index
            if an_code[0] == 'N':
                if idf.strip() != '':
                    try:
                        number = float(idf)
                        if '\\maximum' in idd.meta_data:
                            max_constraint_string = idd.meta_data['\\maximum'][0]
                            if max_constraint_string[0] == "<":
                                max_val = float(max_constraint_string[1:])
                                if number >= max_val:
                                    issues.append(ValidationIssue(
                                        idd_object.name, idd.field_name,
                                        'Field value higher than idd-specified maximum>; actual={}, max={}'.format(
                                            number, max_val)))
                            else:
                                max_val = float(max_constraint_string)
                                if number > max_val:
                                    issues.append(ValidationIssue(
                                        idd_object.name, idd.field_name,
                                        'Field value higher than idd-specified maximum; actual={}, max={}'.format(
                                            number, max_val)))
                        if '\\minimum' in idd.meta_data:
                            min_constraint_string = idd.meta_data['\\minimum'][0]
                            if min_constraint_string[0] == ">":
                                min_val = float(min_constraint_string[1:])
                                if number <= min_val:
                                    issues.append(ValidationIssue(
                                        idd_object.name, idd.field_name,
                                        'Field value lower than idd-specified minimum<; actual={}, max={}'.format(
                                            number, max_val)))
                            else:
                                min_val = float(min_constraint_string)
                                if number < min_val:
                                    issues.append(ValidationIssue(
                                        idd_object.name, idd.field_name,
                                        'Field value lower than idd-specified minimum; actual={}, max={}'.format(
                                            number, max_val)))
                    except ValueError:
                        if '\\autosizable' in idd.meta_data and idf.upper() == 'AUTOSIZE':
                            pass  # everything is ok
                        elif idf.upper() == 'AUTOSIZE':
                            issues.append(ValidationIssue(idd_object.name, idd.field_name,
                                                          'Autosize detected in numeric field that is _not_ listed autosizable'))
                        elif '\\autocalculatable' in idd.meta_data and idf.upper() == 'AUTOCALCULATE':
                            pass  # everything is ok
                        elif idf.upper() == 'AUTOCALCULATE':
                            issues.append(ValidationIssue(idd_object.name, idd.field_name,
                                                          'Autocalculate detected in numeric field that is _not_ listed autocalculatable'))
                        else:
                            issues.append(ValidationIssue(idd_object.name, idd.field_name,
                                                          'Non-numeric value in idd-specified numeric field'))
        return issues

    def write_object(self, file_object):
        """
        This function simply writes out the idf string to a file object

        :param file_object: A file-type object that responds to a write command
        :return: Nothing
        """
        # TODO: Return with something meaningful, use a try block
        file_object.write(self.object_string())


class IDFStructure(object):
    """
    An IDF structure representation.  This includes containing all the IDF objects in the file, as well as meta data
    such as the version ID for this IDD, and finally providing worker functions for accessing the IDD data

    Relevant "public" members are listed here:

    :ivar str file_path: The path given when instantiating this IDF, not necessarily an actual path
    :ivar float version_float: The floating point representation of the version of this IDD (for 8.6.0 it is 8.6)
    :ivar [IDFObject] objects: A list of all IDF objects found in the IDF

    Constructor parameters:

    :param str file_path: A file path for this IDF; not necessarily a valid path as it is never used, just available
                          for bookkeeping purposes.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.version_string = None
        self.version_float = None
        self.objects = None

    def get_idf_objects_by_type(self, type_to_get):
        """
        This function returns all objects of a given type found in this IDF structure instance

        :param str type_to_get: A case-insensitive object type to retrieve
        :return: A list of all objects of the given type
        """
        return [i for i in self.objects if i.object_name.upper() == type_to_get.upper()]

    def whole_idf_string(self, idd_structure=None):
        """
        This function returns a string representation of the entire IDF contents.  If the idd structure argument is
        passed in, it is passed along to object worker functions in order to generate an intelligent representation.

        :param IDDStructure idd_structure: An optional IDDStructure instance representing an entire IDD file
        :return: A string of the entire IDF contents, ready to write to a file
        """
        s = ''
        for idf_obj in self.objects:
            idd_obj = idd_structure.get_object_by_type(idf_obj.object_name)
            s += idf_obj.object_string(idd_obj) + '\n'
        return s

    def write_idf(self, idf_path, idd_structure=None):
        """
        This function writes the entire IDF contents to a file.  If the idd structure argument is
        passed in, it is passed along to object worker functions in order to generate an intelligent representation.

        :param str idf_path: The path to the file to write
        :param IDDStructure idd_structure: An optional IDDStructure instance representing an entire IDD file
        :return: Nothing
        """
        # TODO: use try/except, add proper return type
        with open(idf_path, 'w') as f:
            f.write(self.whole_idf_string(idd_structure))

    def validate(self, idd_structure):
        """
        This function validates the current IDF structure instance against standard IDD object tags such as required
        and unique objects.

        :param idd_structure: An IDDStructure instance representing an entire IDD file
        :return: A list of ValidationIssue instances, each describing an issue encountered
        """
        issues = []
        required_objects = idd_structure.get_objects_with_meta_data('\\required-object')
        for r in required_objects:
            objects = self.get_idf_objects_by_type(r.name)
            if len(objects) == 0:
                issues.append(ValidationIssue(r.name, message="Required object not found in IDF contents"))
        unique_objects = idd_structure.get_objects_with_meta_data('\\unique-object')
        for u in unique_objects:
            objects = self.get_idf_objects_by_type(u.name)
            if len(objects) > 1:
                issues.append(ValidationIssue(u.name, message="Unique object has multiple instances in IDF contents"))
        for idf_object in self.objects:
            if idf_object.comment:
                continue
            idd_object = idd_structure.get_object_by_type(idf_object.object_name)
            this_object_issues = idf_object.validate(idd_object)
            if this_object_issues:
                issues.extend(this_object_issues)
        return issues
