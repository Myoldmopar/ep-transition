import StringIO
import os

from eptransition import epexceptions
from iddobject import IDDField, IDDObject, IDDStructure, IDDGroup


class CurrentReadType:
    EncounteredComment_ReadToCR = 0
    ReadAnything = 1
    ReadingGroupDeclaration = 2
    ReadingObjectName = 3
    LookingForObjectMetaDataOrNextField = 4
    ReadingObjectMetaData = 5
    ReadingObjectMetaDataContents = 6
    ReadingFieldANValue = 7
    ReadingFieldMetaData = 8
    ReadingFieldMetaDataOrNextANValue = 9
    LookingForFieldMetaDataOrNextObject = 10
    LookingForFieldMetaDataOrNextField = 11


class IDDProcessor:
    def __init__(self):
        self.idd = None
        self.idd_file_stream = None
        self.file_path = None
        self.group_flag_string = "\\group"
        self.obj_flags = ["\\memo", "\\unique-object", "\\required-object", "\\min-fields",
                          "\\obselete", "\\extensible", "\\format"]
        self.field_flags = ["\\field", "\\note", "\\required-field", "\\begin-extensible", "\\unitsBasedOnField",
                            "\\units", "\\ip-units", "\\scheduleunits", "\\minimum", "\\maximum", "\\default",
                            "\\deprecated", "\\autosizable", "\\autocalculatable", "\\type", "\\retaincase",
                            "\\key", "\\object-list", "\\reference", "\\external-list"]

    def process_file_given_file_path(self, file_path):
        if not os.path.exists(file_path):
            raise epexceptions.ProcessingException("Input IDD file not found=\"" + file_path + "\"")  # pragma: no cover
        self.idd_file_stream = open(file_path, 'r')
        self.file_path = file_path
        return self.process_file()

    def process_file_via_stream(self, idd_file_stream):
        self.idd_file_stream = idd_file_stream
        self.file_path = "/streamed/idd"
        return self.process_file()

    def process_file_via_string(self, idd_string):
        self.idd_file_stream = StringIO.StringIO(idd_string)
        self.file_path = "/string/idd/snippet"
        return self.process_file()

    def peek_one_char(self):
        pos = self.idd_file_stream.tell()
        c = self.idd_file_stream.read(1)
        if c == '':
            c = None
        self.idd_file_stream.seek(pos)
        return c

    def read_one_char(self):
        c = self.idd_file_stream.read(1)
        if c == '':
            c = None
        return c

    def process_file(self):

        # flags and miscellaneous variables
        line_index = 1  # 1-based counter for the current line of the file
        last_field_for_object = False  # this will be the last field if a semicolon is encountered

        # variables used as we are building the input structure
        self.idd = IDDStructure(self.file_path)  # empty overall IDD structure
        cur_group = None  # temporary placeholder for an IDD group
        cur_object = None  # temporary placeholder for an IDD object
        cur_field = None  # temporary placeholder for an IDD field
        cur_obj_meta_data_type = None  # temporary placeholder for the type of object metadata encountered

        # variables related to building and processing tokens
        token_builder = ''

        # state machine variables
        read_status = CurrentReadType.ReadAnything  # current state machine reading status
        revert_status_after_comment = None  # reading status before the comment, shift back to this after comment's done

        # loop continuously, the loop will exit when it is done
        while True:

            # update the next character
            just_read_char = self.read_one_char()
            if not just_read_char:
                break

            # update the peeked character
            peeked_char = self.peek_one_char()
            if not peeked_char:
                peeked_char = '\n'  # to simulate that the line ended

            # jump if we are at an EOL
            if just_read_char == '\n':
                # increment the counter
                line_index += 1

            # if we aren't already processing a comment, and we have a comment:
            #  don't append to the token builder, just set read status
            if read_status != CurrentReadType.EncounteredComment_ReadToCR:
                if just_read_char == '!':
                    if read_status != CurrentReadType.ReadingFieldMetaData:
                        read_status = CurrentReadType.EncounteredComment_ReadToCR
                else:
                    token_builder += just_read_char

            # clear a preceding line feed character from the token
            if just_read_char == '\n' and len(token_builder) == 1:
                token_builder = ''

            if read_status == CurrentReadType.ReadAnything:

                # this is the most general case where we are wandering through the IDD looking for whatever
                # the possibilities are: comments, group declaration, or object definition
                if peeked_char == "\\":  # starting a group name
                    read_status = CurrentReadType.ReadingGroupDeclaration
                elif peeked_char in [" ", '\n', '\t']:  # don't do anything
                    pass
                elif peeked_char == "!":
                    revert_status_after_comment = read_status
                    read_status = CurrentReadType.EncounteredComment_ReadToCR
                else:  # should be alphanumeric, just start reading object name
                    read_status = CurrentReadType.ReadingObjectName

            elif read_status == CurrentReadType.ReadingGroupDeclaration:

                # for the group declarations, we will just check to see if the
                # line has ended since it should be on a single line
                # if it hasn't then just keep on as is, if it has, parse the group name out of it
                if peeked_char == '\n':
                    # first update the previous group
                    if cur_group is not None:
                        self.idd.groups.append(cur_group)
                    group_declaration = token_builder
                    group_flag_index = group_declaration.find(self.group_flag_string)
                    if group_flag_index == -1:  # pragma: no cover
                        # add error to error report
                        raise epexceptions.ProcessingException(
                            "Group keyword not found where expected",
                            line_index=line_index)
                    else:
                        group_declaration = group_declaration[len(self.group_flag_string):]
                    cur_group = IDDGroup(group_declaration.strip())
                    token_builder = ""
                    read_status = CurrentReadType.ReadAnything  # to start looking for groups/objects/comments/whatever

            elif read_status == CurrentReadType.ReadingObjectName:

                # the object names could have several aspects
                # they could be a single line object, such as: "Lead Input;"
                # they could be the title of a multi field object, such as: "Version,"
                # and they could of course have comments at the end
                # for now I will assume that the single line objects can't have metadata
                # so read until either a comma or semicolon, also trap for errors if we reach the end of line or comment
                if peeked_char == ",":
                    object_title = token_builder
                    cur_object = IDDObject(object_title)
                    token_builder = ''
                    self.read_one_char()  # to clear the comma
                    read_status = CurrentReadType.LookingForObjectMetaDataOrNextField
                elif peeked_char == ";":
                    # since this whole object is a single line, we can just add it directly to the current group
                    object_title = token_builder
                    # this is added to singleline objects because CurGroup isn't instantiated yet, should fix
                    self.idd.single_line_objects.append(object_title.strip())
                    token_builder = ''  # to clear the builder
                    self.read_one_char()  # to clear the semicolon
                    read_status = CurrentReadType.ReadAnything
                elif peeked_char in ['\n', '!']:  # pragma: no cover
                    raise epexceptions.ProcessingException(
                        "An object name was not properly terminated by a comma or semicolon",
                        line_index=line_index)

            elif read_status == CurrentReadType.LookingForObjectMetaDataOrNextField:

                token_builder = ''
                if peeked_char == '\\':
                    read_status = CurrentReadType.ReadingObjectMetaData
                elif peeked_char in ['A', 'N']:
                    read_status = CurrentReadType.ReadingFieldANValue
                elif peeked_char == '!':
                    revert_status_after_comment = read_status
                    read_status = CurrentReadType.EncounteredComment_ReadToCR
                elif peeked_char == ' ':
                    # just let it keep reading
                    pass
                elif peeked_char == '\n':
                    # just let it keep reading
                    pass

            elif read_status == CurrentReadType.ReadingObjectMetaData:

                if peeked_char in [' ', ':', '\n']:
                    if token_builder in self.obj_flags:
                        cur_obj_meta_data_type = token_builder
                        token_builder = ''
                        if cur_obj_meta_data_type in ['\\obselete', '\\required-object', '\\unique-object']:
                            # these do not carry further data, stop reading now
                            if cur_obj_meta_data_type not in cur_object.meta_data:
                                string_list = [None]
                                cur_object.meta_data[cur_obj_meta_data_type] = string_list
                            else:  # pragma: no cover   -- strings already exist, this is not valid...
                                raise epexceptions.ProcessingException(
                                    "Erroneous object meta data - repeated \"" + token_builder + "\"",
                                    line_index=line_index,
                                    object_name=cur_object.name)
                            cur_obj_meta_data_type = None
                            read_status = CurrentReadType.LookingForObjectMetaDataOrNextField
                        else:
                            # these will have following data, just set the flag
                            read_status = CurrentReadType.ReadingObjectMetaDataContents
                    else:  # pragma: no cover
                        # token_builder = ''
                        raise epexceptions.ProcessingException(
                            "Erroneous object meta data tag found",
                            line_index=line_index,
                            object_name=cur_object.name)
                else:
                    # just keep reading
                    pass

            elif read_status == CurrentReadType.ReadingObjectMetaDataContents:

                if peeked_char == '\n':
                    data = token_builder.strip()
                    if cur_obj_meta_data_type not in cur_object.meta_data:
                        string_list = [data]
                        cur_object.meta_data[cur_obj_meta_data_type] = string_list
                    else:
                        string_list = cur_object.meta_data[cur_obj_meta_data_type]
                        string_list.append(data)
                        cur_object.meta_data[cur_obj_meta_data_type] = string_list
                    token_builder = ''
                    cur_obj_meta_data_type = None
                    read_status = CurrentReadType.LookingForObjectMetaDataOrNextField

            elif read_status == CurrentReadType.ReadingFieldANValue:

                if peeked_char in [',', ';']:
                    cur_field = IDDField(token_builder.strip())
                    token_builder = ''
                    if peeked_char == ',':
                        last_field_for_object = False
                    elif peeked_char == ';':
                        last_field_for_object = True
                    read_status = CurrentReadType.ReadingFieldMetaDataOrNextANValue
                elif peeked_char == '\n':  # pragma: no cover
                    raise epexceptions.ProcessingException(
                        "Blank or erroneous ""AN"" field index value",
                        line_index=line_index,
                        object_name=cur_object.name)

            elif read_status == CurrentReadType.ReadingFieldMetaDataOrNextANValue:

                if peeked_char == '\\':
                    token_builder = ''
                    read_status = CurrentReadType.ReadingFieldMetaData
                elif peeked_char in ['A', 'N']:
                    token_builder = ''
                    # this is hit when we have an AN value right after a previous AN value, so no meta data is added
                    cur_object.fields.append(cur_field)
                    read_status = CurrentReadType.ReadingFieldANValue

            elif read_status == CurrentReadType.ReadingFieldMetaData:

                if peeked_char == '\n':

                    # for this one, let's read all the way to the end of the line, then parse data
                    flag_found = next((x for x in self.field_flags if x in token_builder), None)
                    if flag_found:
                        data = token_builder[len(flag_found):]
                        # data needs to start with a space, otherwise things like: \fieldd My Field would be valid
                        if len(data) > 0:
                            if data[0] not in [' ', '>', '<']:
                                raise epexceptions.ProcessingException(
                                    'Invalid meta data, expected a space after the meta data specifier before the data',
                                    line_index=line_index,
                                    object_name=cur_object.name,
                                    field_name=cur_field.field_name
                                )
                        data = data.strip()
                        if flag_found == '\\field':
                            cur_field.field_name = data
                        else:
                            if flag_found not in cur_field.meta_data:
                                string_list = [data]
                                cur_field.meta_data[flag_found] = string_list
                            else:
                                string_list = cur_field.meta_data[flag_found]
                                string_list.append(data)
                                cur_field.meta_data[flag_found] = string_list
                    else:  # pragma: no cover
                        raise epexceptions.ProcessingException(
                            "Erroneous field meta data entry found",
                            line_index=line_index,
                            object_name=cur_object.name,
                            field_name=cur_field.field_name)
                    token_builder = ''
                    if last_field_for_object:
                        read_status = CurrentReadType.LookingForFieldMetaDataOrNextObject
                    else:
                        read_status = CurrentReadType.LookingForFieldMetaDataOrNextField

                else:
                    # just keep reading
                    pass

            elif read_status == CurrentReadType.LookingForFieldMetaDataOrNextField:

                if peeked_char in ['A', 'N']:
                    token_builder = ''
                    cur_object.fields.append(cur_field)
                    read_status = CurrentReadType.ReadingFieldANValue
                elif peeked_char == '\\':
                    token_builder = ''
                    read_status = CurrentReadType.ReadingFieldMetaData
                elif peeked_char == '!':
                    revert_status_after_comment = read_status
                    read_status = CurrentReadType.EncounteredComment_ReadToCR
                elif peeked_char == '\n':
                    # just let it keep reading
                    pass

            elif read_status == CurrentReadType.LookingForFieldMetaDataOrNextObject:

                if peeked_char == '\\':
                    token_builder = ''
                    read_status = CurrentReadType.ReadingFieldMetaData

                elif peeked_char == '\n':
                    # blank line will mean we are concluding this object
                    token_builder = ''
                    cur_object.fields.append(cur_field)
                    cur_group.objects.append(cur_object)
                    read_status = CurrentReadType.ReadAnything

            elif read_status == CurrentReadType.EncounteredComment_ReadToCR:

                # set the flag for reading the next line if necessary
                token_builder += just_read_char
                if peeked_char == '\n':
                    if revert_status_after_comment is not None:
                        read_status = revert_status_after_comment
                        revert_status_after_comment = None
                    else:
                        read_status = CurrentReadType.ReadAnything
                    token_builder = ''

                    # don't ever put code here that could have side effects,
                    # as the blocks are not required to call continue when they are done

        # end the file here, but should watch for end-of-file in other CASEs also
        # cur_object.fields.append(cur_field)
        # cur_group.objects.append(cur_object)
        self.idd.groups.append(cur_group)

        return self.idd
