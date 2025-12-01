from pathlib import Path
from pandas import Timestamp

# PATHS
MAIN_PATH = Path().cwd()
JSON_PATH: str = f"{MAIN_PATH}/data/json_data"
COMMON_DB_PATH: str = f"{MAIN_PATH}/infrastructure/db/common_data.db"
SERV_DB_PATH: str = f"{MAIN_PATH}/infrastructure/db/services_data.db"
DB_PATH: str = f"sqlite:///{MAIN_PATH}/infrastructure/db/data.db"

# DATES
PAGE_STRFTIME_DMY = "%d/%m/%Y"
PAGE_STRFTIME_YMD = "%Y/%m/%d"
FILE_STRFTIME_DMY = "%d-%m-%Y"
FILE_STRFTIME_YMD = "%Y-%m-%d"
DELTA_STRFTIME_YM = "%Y-%m"
DELTA_STRFTIME_MY = "%m-%Y"

TODAY_DATE_PAGE = Timestamp.today().strftime(PAGE_STRFTIME_DMY)
TODAY_DATE_FILE_DMY = Timestamp.today().strftime(FILE_STRFTIME_DMY)
TODAY_DATE_FILE_YMD = Timestamp.today().strftime(FILE_STRFTIME_YMD)
TODAY_FOR_DELTA = Timestamp.today().strftime(DELTA_STRFTIME_YM)



