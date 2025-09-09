from enum import Enum

class WithZeroEnum(Enum):
    ZERO = "ZERO"
    NON_ZERO = "NON ZERO"

class SaveEnum(Enum):
    SAVE = "SAVE"
    NOT_SAVE = "NOT SAVE"

class IndexTypeEnum(Enum):
    BY_MOTOR = "MOTOR"
    BY_VEHICLE = "VEHICLE"

class ScrapEnum(Enum):
    WEB_SCRAP = "WEB"
    LOCAL_SCRAP = "LOCAL"

class ExcelEnum(Enum):
    WITH_EXCEL = "WITH EXCEL" 
    WITHOUT_EXCEL = "WITHOUT EXCEL"
