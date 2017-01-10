class CurrentReadType:
    EncounteredComment_ReadToCR = 0
    ReadAnything = 1
    ReadingGroupDeclaration = 2
    ReadingObjectName = 3
    LookingForObjectMetaDataOrNextField = 4  # check for "\" or an alphanumeric character
    ReadingObjectMetaData = 5
    ReadingObjectMetaDataContents = 6
    ReadingFieldANValue = 7
    ReadingFieldMetaData = 8
    ReadingFieldMetaDataOrNextANValue = 9
    ReadingSpecialFieldMetaData = 10
    LookingForFieldMetaDataOrNextObject = 11
    LookingForFieldMetaDataOrNextField = 12
    NumberOfReadTypes = 12


class ObjFlagEnum:
    Memo = 0
    UniqueObject = 1
    RequiredObject = 2
    MinFields = 3
    Obselete = 4
    Extensible = 5
    Format = 6


class FieldFlagEnum:
    Field = 0
    Note = 1
    RequiredField = 2
    BeginExtensible = 3
    Units = 4
    IPUnits = 5
    ScheduleUnits = 6
    Minimum = 7
    Maximum = 8
    Default = 9
    Deprecated = 10
    AutoSizable = 11
    AutoCalculatable = 12
    Type = 13
    RetainCase = 14
    Key = 15
    ObjectList = 16
    Reference = 17
    ExternalList = 18
    Memo = 18  # note memo isn't supposed to be a field flag, but it is in there as such for some objects
