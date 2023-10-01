from config import *
import re, gspread

############################################################
#   　　　　　      　　　　　　　　　　　　                  #
#               gspread のデータベースのクラス               #
#   　　　　　      　　　　　　　　　　　　                  #
############################################################
class databaseError(Exception):
    pass

class database:
    """
    The class that manages the spreadsheet as simplified database
    
    :vars existingWord: After obtaining the ID of the guild,
                    a dictionary of keys and values of the registered guilds
                    will be entered.
                    When the class is generated, it is a empty dictionary.
                    Therefore, the chooseServer function must be executed
                    to populate this list before any operations are performed:
                    unless it is specified as a class argument.
        :type dataList: dict
    :vars dataList: After getting the ID of the guild, a list
                    of registered guild values will be included.
                    When the class is generated, it is a empty list.
                    Therefore, the chooseServer function must be executed
                    to populate this list before any operations are performed:
                    unless it is specified as a class argument.
        :type dataList: list
    :vars dictionaries: This is an internal variable that contains
                    the sheet where data in dictionary format is stored.
                    By default, information handled within a class is
                    handled in this variable as a dictionary format.
                    The information contained in this variable is only that of the sheet,
                    and when used outside of the class, the more detailed object
                    provided by the method should be handled.
    :vars lists: This is an internal variable that contains
                    the sheet where data in list format is stored.
                    Same as 'dictionaries' variable.
    :vars guildRow: Returns the row of the guild passed in the sheet.
                    This value is the number of rows in the spreadsheet,
                    counted from row 1. Note: however, that the first row
                    of the sheet is the title of the item.
        :type guildRow: int | None
    :vars workbook: An internal variable that contains the spread sheet file
                    that will be the database. It is set only once in the initializer
                    and is not intended to be changed. The file to be read is
                    contained inthe fileOfVar variable, which is described in config.py.
    :func chooseGuild: Register your guild in the class. Must be performed
                    when manipulating the database.
    :func GetDictValue:
    :func SetDictValue:
    :func DeleteDictData:
    :func GetListValue:
    :func SetListValue:

    :args sheet: Which sheet's database to create. This is specified
                    by the name of the sheet.
        :type sheet: str
    :args type: Dictionary or List
        :type type: str
    :args guild: Guild ID of the data to be handled
        :type guild: int

    :raise databaseError: Something error happend
    """

    def __init__(self, sheet: str, *, type: str = "list", guild: int = None) -> None:
        """
        The initializer function called when the argument 'sheet' has a string value
        """
        self.guildRow = None
        self.type = type
        self.workbook = gc.open_by_key(fileOfVar)
        if type == "dict":
            try:
                self.dictionaries = self.workbook.worksheet(sheet)
            except gspread.WorksheetNotFound:
                raise databaseError("Invalid value inserted for argument 'type'")
        elif type == "list":
            try:
                self.lists = self.workbook.worksheet(sheet)
            except gspread.WorksheetNotFound:
                raise databaseError("Invalid value inserted for argument 'type'")
        else:
            raise databaseError("Invalid value inserted for argument 'type'")
        self.dataList = []
        self.existingWord = {}
        if guild is not None:
            self.ChooseGuild(guild)

    @property
    def guildRow(self):
        if self._guildRow is None:
            raise databaseError("'guildRow' returned None")
        return self._guildRow
    
    @guildRow.setter
    def guildRow(self, value):
        self._guildRow = value

    def ChooseGuild(self, guildID: int) -> int:
        if self.type == "list":
            sheet = self.lists
        elif self.type == "dict":
            sheet = self.dictionaries
        else:
            raise databaseError("'type' is invalid")
        if str(guildID) in sheet.col_values(1):
            self.guildRow = sheet.find(str(guildID)).row
        else:
            self.guildRow = len(sheet.col_values(1)) + 1
            sheet.update_cell(self.guildRow, 1, str(guildID))
        return self.guildRow


    @property
    def GetAllDict(self):
        return self.dictionaries.row_values(self.guildRow)[1:]

    def GetDictValue(self, key: str):
        self.dataList = self.dictionaries.row_values(self.guildRow)
        self.existingWord = {i: prevData for i, prevData in enumerate(self.dataList) if re.match(f'{key}:(.+)', prevData)}
        return self.existingWord if self.existingWord else None

    def SetDictValue(self, key: str, value: str):
        self.dataList = self.dictionaries.row_values(self.guildRow)
        if self.GetDictValue(key) == None:
            self.dictionaries.update_cell(self.guildRow, len(self.dataList) + 1, f'{key}:{value}')
        elif len(self.GetDictValue(key)) == 1:
            self.dictionaries.update_cell(self.guildRow, self.GetDictValue(key).keys[0], f'{key}:{value}')
        elif len(self.GetDictValue(key)) >= 2:
            raise databaseError("Duplicate key is registered in the database")
        else:
            raise databaseError("An unexpected error occurred in retrieving the dictionary")

    def DeleteDictData(self, key: str):
        self.dataList = self.dictionaries.row_values(self.guildRow)
        if self.GetDictValue(key) == None:
            return None
        elif len(self.GetDictValue(key)) == 1:
            self.dictionaries.update_cell(self.guildRow, self.GetDictValue(key).keys[0], "")
        elif len(self.GetDictValue(key)) >= 2:
            raise databaseError("Duplicate key is registered in the database")


    @property
    def GetIndexTitle(self):
        return self.lists.row_values(1)[1:]

    @property
    def GetTotalIndex(self):
        return len(self.lists.row_values(1))

    def GetListValue(self, index: int):
        if index > (len(self.GetIndexTitle) + 1):
            raise OverflowError(f"dataList index out of range: length of 'dataList' is {(len(self.GetIndexTitle) + 1)}")
        existingStringList = self.lists.row_values(self.guildRow)
        existingStringList += ['' for i in range(self.GetTotalIndex - len(existingStringList))]
        self.existingString = existingStringList[index - 1]
        return self.existingString if self.existingString else None

    def SetListValue(self, index: int, data: str):
        self.dataList = self.lists.row_values(self.guildRow)
        self.dataList += ['' for i in range(self.GetTotalIndex - len(self.dataList))]
        if index > (len(self.dataList) + 1):
            raise OverflowError(f"dataList index out of range: length of 'dataList' is {(len(self.dataList) + 1)}")
        self.lists.update_cell(self.guildRow, index, data)

    def SetListValue(self, index: int):
        self.dataList = self.lists.row_values(self.guildRow)
        self.dataList += ['' for i in range(self.GetTotalIndex - len(self.dataList))]
        if index > (len(self.dataList) + 1):
            raise OverflowError(f"dataList index out of range: length of 'dataList' is {(len(self.dataList) + 1)}")
        self.lists.update_cell(self.guildRow, index)

############################################################
#   　　　　　      　　　　　　　　　　　　                  #
#                       便利系小ツール                      #
#   　　　　　      　　　　　　　　　　　　                  #
############################################################

def replace(text, *args) -> str:
    """
    Replace $n in text with args

    Examples
    --------
    >>> replace("$1は$2にある$3です", "富士山", "静岡県と山梨県", "山")
    "富士山は静岡県と山梨県にある山です"

    Returns
    --------
    :type text: str
    """
    i = 1
    for afterText in args:
        beforeText = '$' + str(i)
        text = text.replace(beforeText, str(afterText))
        i += 1
    return text

def ramification(bool: bool, text: str, another: str, position: int = None, endPosition: int = None) -> str:
    """
    Returns different text depending on the bool value
    If bool is True, text is returned as is; otherwise, another is returned. If position is specified, another is substituted from the location specified in text

    :args bool: True or False
        :type bool: bool
    :args text: original text
        :type text: str
    :args another: another text
        :type another: str
    :args position: replace position
        :type position: int
    """
    if bool:
        return text
    else:
        if (position is not None) and (endPosition is not None):
            if position > len(text):
                raise IndexError("the position specified exceeds the length of the text")
            text = text[:position] + another + text[endPosition:]
            return text

        if (position is not None) and (endPosition is None):
            text = text[:position] + another
            return text
        
        elif (position is None) and (endPosition is not None):
            text = another + text[:position]
            return text

        elif (position is None) and (endPosition is None):
            return another


def mostPopular(list):
    totalDict = collections.Counter(list)
    mostPopular = [kv[0] for kv in totalDict.items() if kv[1] == max(totalDict.values())]
    finallyObject = random.choice(mostPopular)
    return finallyObject
