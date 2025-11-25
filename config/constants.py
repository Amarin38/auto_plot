from typing import Tuple, List
from pathlib import Path
from pandas import Timestamp

# Inventory cleaner
INTERNOS_DEVOLUCION: List[str] = ["C0488", "C0489", "C0500", "C0700", "C1400",
                                  "C4500", "C4900", "C6000", "C6700", "C9500",
                                  "C9100", "C7000", "C5000", "C9000", "C3000",
                                  "C4800", "C4700", "U4000", "C6600", "C6400",
                                  "C0199", "C0599", "C0799", "C1499", "C4599",
                                  "C4999", "C6099", "C6799", "C9599", "C9199",
                                  "C7099", "C5099", "C9099", "C3099", "C4899",
                                  "C4799", "C5599", "C6699", "C6199", "U1111"]

DEL_COLUMNS: List[str] = ["artipo", "ficdep", "fictra",
                          "movnom", "ficpro", "pronom",
                          "ficrem", "ficfac","corte",
                          "signo", "transfe"]

FORECAST_TREND_COLUMNS: List[str] = ["Repuesto", "TipoRepuesto", "FechaCompleta",
                                     "Año", "Mes", "Tendencia", "TendenciaEstacional"]

FORECAST_DATA_COLUMNS: List[str] = ["Repuesto", "TipoRepuesto", "FechaCompleta", "Año", "Mes",
                                    "TotalAño", "TotalMes", "Promedio", "IndiceAnual", "IndiceEstacional"]

# Filtro
FILTRO_OBS = "0KM|TRANSMISIÓN|CAMBIO"

# MOVS
MOV_SALIDAS: str = "TRD|DES"
# MOV_ENTRADAS: str = "Tranf desde |Transf Recibida|Entrada "
MOV_ENTRADAS: str = "COM|TRA"
MOV_DEVOLUCIONES: str = "DEU|DEC"

# View Config.
MAIN_TABS: Tuple[str, ...] = (" 🏠 Página principal", " 📊 Índices de consumo",
                              " 📈 Previsión de consumo", " 📊 Desviación de índices",
                              " 🚫 Falla Garantías", " ↕️ Máximos y Mínimos")


PAG_PRINCIPAL = "Página principal 🏠"

# Pags Generales
PAG_CARGAR_DATOS = "Cargar datos 🔄️"
PAG_INDICES = "Índices de consumo 📊"
PAG_HISTORIAL = "Historial de consumos 💽"
PAG_CONSUMO_OBLIGATORIO = "Consumo Obligatorio 🚨"
PAG_PREVISION = "Previsión de consumo 📈"
PAG_DESVIACION_INDICES = "Desviaciones de índices 📊"
PAG_DURACION = "Duracion de repuestos 🛠️"
PAG_FALLA_GARANTIAS = "Falla equipos garantías ⛔"
PAG_MAXIMOS_MINIMOS = "Máximos y Mínimos ⬆️⬇️"
PAG_COCHES_CABECERA = "Coches por cabecera 🚌"

# Pags Gomeria
PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS = "Transferencias entre depósitos 🔃"

# Tabs
TABS_FALLAS = ("🚫 Falla Equipos Garantías", "📊 Consumos Garantias y Transferencias")
TABS_DURACION = ("🛠️ General", "🔧 Por repuesto")

# Selectboxes
PLACEHOLDER = "------"


# HEIGHT
PIE_PLOT_HEIGHT: int = 585
DATAFRAME_HEIGHT: int = 600
LINK_BOX_HEIGHT: int = 72
SELECT_BOX_HEIGHT: int = 120
CENTERED_TITLE_HEIGHT: int = 78
BARPLOT_BOX_HEIGHT: int = 700
PLOT_BOX_HEIGHT: int = 535
PIE_PLOT_BOX_HEIGHT: int = 700
MULTIPLE_PLOT_BOX_HEIGHT: int = 700
FULL_PLOT_BOX_HEIGHT: int = 650
FULL_PLOT_BOX_TRANSFER_HEIGHT: int = 610
TEXT_BOX_HEIGHT: int = 450
TAB_BOX_HEIGHT: int = 770
DURACION_TAB_BOX_HEIGHT: int = 955
DESVIACION_BOX_HEIGHT: int = 685
FILE_UPLOADER_HEIGHT: int = 368
FALLA_TAB_BOX_HEIGHT: int = 870
FALLA_GARANTIAS_BOX_HEIGHT: int = 700


# WIDTH
PIE_PLOT_WIDTH: int = 585
BARPLOT_WIDTH: int = 1100
LINK_BOX_WIDTH: int = 350
SELECT_BOX_WIDTH: int = 650
CENTERED_TITLE_WIDTH: int = 570
BARPLOT_BOX_WIDTH: int = 1600
PIE_PLOT_BOX_WIDTH: int = 1550


# FONT
PIE_FONT_SIZE: int = 24


# DISTANCE
DISTANCE_COLS_SELECT_PLOT: Tuple[int, int] = (1, 5)
DISTANCE_COLS_DUAL_PLOT: Tuple[int, float] = (1, 1.8)
DISTANTE_COLS_DUAL_SELECT: Tuple[int, float] = (1, 0.5)

DISTANCE_COLS_SELECTBIGGER_PLOT: Tuple[float, int] = (0.70, 3)
DISTANCE_COLS_CENTER_TITLE: Tuple[float, int, int] = (0.95, 3, 1)


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
TODAY_DATE_FILE = Timestamp.today().strftime(FILE_STRFTIME_DMY)
TODAY_FOR_DELTA = Timestamp.today().strftime(DELTA_STRFTIME_YM)




# Colors
COLORS: Tuple[str, ...] = ("#F2C14E", "#FF5733", "#C70039", "#900C3F", "#5C6D70",
                           "#2C2C54", "#5FAD56", "#FFC300", "#F78154", "#4D9078",
                           "#4A1942", "#823329", "#3F7CAC", "#899878", "#5497A7", 
                           "#883677", "#3A7D44", "#254D32", "#F7CE5B", "#F7B05B",
                           "#414770", "#5E6973", "#0E1117", "#2B303A", "#0C7C59",
                           "#C44900", "#3D4044")

INDICE_COLORS: Tuple[str, ...] = ("#5497A7", "#C70039", "#900C3F", "#5C6D70", "#414770",
                                  "#0C7C59", "#823329", "#883677", "#F78154", "#FE5F55",
                                  "#0A2342", "#2CA58D", "#502F4C", "#9C88AC", "#225560",
                                  "#E39774", "#698F3F", "#804E49", "#B0413E", "#226F54",
                                  "#A4031F", "#7D8491")

INDICE_MEDIA_COLOR: str = "#FF5733"

FALLAS_GARANTIAS_COLORS: Tuple[str, ...] = ("#F1D764", "#F4A259", "#5B8E7D", "#BC4B51", "#897AEA")
CONSUMO_GARANTIAS_COLORS: Tuple[str, str] = ("#C70039","#0C7C59")



# HTML
HTML_SIN_CAMBIOS = """<p style='
                    color: #5497A7; 
                    font: bold light 18px sans-serif;
                    background: #0E1117; 
                    border-radius: 5px;
                    border-width: 2px;
                    border-style: solid; 
                    border-color: #3D4044;
                    text-align: center'>"""


# TEXT COLORS
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


# BACKGROUND COLORS
B_RED = '\033[41m'
B_ORANGE = '\033[48;5;208m'


# TEXT MODS
UNDERLINE = '\033[4m'
ITALIC = '\033[3m'
DIMM = '\033[22m'
RESET = '\033[0m'

