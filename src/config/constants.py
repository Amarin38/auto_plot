from typing import Tuple
from pathlib import Path
from pandas import Timestamp

# Inventory cleaner
INTERNOS_DEVOLUCION: Tuple[str, ...] = ("C0488", "C0489", "C0500", "C0700", "C1400", 
                                        "C4500", "C4900", "C6000", "C6700", "C9500",
                                        "C9100", "C7000", "C5000", "C9000", "C3000",
                                        "C4800", "C4700", "U4000", "C6600", "C6400",
                                        "C0199", "C0599", "C0799", "C1499", "C4599", 
                                        "C4999", "C6099", "C6799", "C9599", "C9199",
                                        "C7099", "C5099", "C9099", "C3099", "C4899", 
                                        "C4799", "C5599", "C6699", "C6199", "U1111")


DEL_COLUMNS: Tuple[str, ...] = ("ficdep", "fictra", "artipo", "ficpro", 
                                "pronom", "ficrem", "ficfac", "corte", 
                                "signo", "transfe", "ficmov")


FORECAST_TREND_COLUMNS: Tuple[str, ...] = ("Repuesto", "TipoRepuesto", "FechaCompleta",
                                           "Año", "Mes", "Tendencia", "TendenciaEstacional") 


FORECAST_DATA_COLUMNS: Tuple[str, ...] = ("Repuesto", "TipoRepuesto", "FechaCompleta", "Año", "Mes", 
                                           "TotalAño", "TotalMes", "Promedio", "IndiceAnual", "IndiceEstacional")


# View Config.
MAIN_TABS: Tuple[str, ...] = (" 🏠 Página principal", " 📊 Índices de consumo",
                              " 📈 Previsión de consumo", " 📊 Desviación de índices",
                              " 🚫 Falla Garantías", " ↕️ Máximos y Mínimos")

# Selectboxes
PLACEHOLDER = "------"

PIE_PLOT_HEIGHT = 650
PIE_PLOT_WIDTH = 650

BARPLOT_WIDTH: int = 1100

DATAFRAME_HEIGHT: int = 600

LINK_BOX_HEIGHT: int = 72
SELECT_BOX_HEIGHT: int = 100
SELECT_BOX_WIDTH: int = 650

BARPLOT_BOX_HEIGHT: int = 700
BARPLOT_BOX_WIDTH: int = 1600

PLOT_BOX_HEIGHT: int = 600

PIE_PLOT_BOX_HEIGHT: int = PLOT_BOX_HEIGHT + 100
PIE_PLOT_BOX_WIDTH: int = PIE_PLOT_WIDTH + 900

MULTIPLE_PLOT_BOX_HEIGHT: int = PLOT_BOX_HEIGHT + 100
FULL_PLOT_BOX_HEIGHT: int = 650

TEXT_BOX_HEIGHT: int = 450
TAB_BOX_HEIGHT: int = FULL_PLOT_BOX_HEIGHT + 100
FALLA_TAB_BOX_HEIGHT: int = TAB_BOX_HEIGHT + 40
FILE_UPLOADER_HEIGHT: int = 368

DISTANCE_COLS_SELECT_PLOT: Tuple[int, int] = (1, 5)
DISTANCE_COLS_SELECTBIGGER_PLOT: Tuple[int, float] = (1, 4.5)
DISTANCE_COLS_DUAL_PLOT: Tuple[int, float] = (1, 1.8)
DISTANTE_COLS_DUAL_SELECT: Tuple[int, float] = (1, 0.5)


# Paths
MAIN_PATH = Path().cwd()
JSON_PATH: str = f"{MAIN_PATH}/src/data/json_data"
COMMON_DB_PATH: str = f"{MAIN_PATH}/src/db_data/db/common_data.db"
SERV_DB_PATH: str = f"{MAIN_PATH}/src/db_data/db/services_data.db"


# Dates
PAGE_STRFTIME_DMY = "%d/%m/%Y"
PAGE_STRFTIME_YMD = "%Y/%m/%d"
FILE_STRFTIME_DMY = "%d-%m-%Y"
FILE_STRFTIME_YMD = "%Y-%m-%d"
DELTA_STRFTIME_YM = "%Y-%m"
DELTA_STRFTIME_MY = "%m-%Y"
TODAY_DATE_PAGE = Timestamp.today().strftime(PAGE_STRFTIME_DMY)
TODAY_DATE_FILE = Timestamp.today().strftime(FILE_STRFTIME_DMY)
TODAY_FOR_DELTA = Timestamp.today().strftime(DELTA_STRFTIME_YM)


# Movs
MOV_SALIDAS: str = "Transf al Dep |Salida"
MOV_ENTRADAS: str = "Tranf desde |Transf Recibida|Entrada "
MOV_DEVOLUCIONES: str = "Devolucion"


# Colors
COLORS: Tuple[str, ...] = ("#FFC300", "#FF5733", "#C70039", "#900C3F", "#5C6D70",
                           "#2C2C54", "#5FAD56", "#F2C14E", "#F78154", "#4D9078",
                           "#4A1942", "#823329", "#3F7CAC", "#899878", "#5497A7", 
                           "#883677", "#3A7D44", "#254D32", "#F7CE5B", "#F7B05B")


# Text colors
T_RED = '\033[91m'
T_LIGHT_RED = '\033[31m'
T_GREEN = '\033[92m'
T_LIGHT_GREEN = '\033[32m'
T_YELLOW = '\033[33m'
T_BLUE = '\033[94m'
T_PURPLE = '\033[95m'
T_CYAN = '\033[96m'
T_WHITE = '\033[97m'
T_BLACK = '\033[90m'
T_MAGENTA = '\033[35m' 
T_GRAY = '\033[90m'
T_ORANGE = '\033[38;5;208m'
T_FUCHSIA = '\033[38;5;170m'

# Background colors
B_RED = '\033[41m'
B_ORANGE = '\033[48;5;208m'

# Text mods.
UNDERLINE = '\033[4m'
ITALIC = '\033[3m'
DIMM = '\033[22m'
RESET = '\033[0m'

