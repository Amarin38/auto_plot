from typing import Tuple, List
from pathlib import Path
import pandas as pd

INTERNOS_DEVOLUCION: Tuple[str, ...] = ("C0488", "C0489", "C0500", "C0700", "C1400", 
                                        "C4500", "C4900", "C6000", "C6700", "C9500",
                                        "C9100", "C7000", "C5000", "C9000", "C3000",
                                        "C4800", "C4700", "U4000", "C6600", "C6400",
                                        "C0199", "C0599", "C0799", "C1499", "C4599", 
                                        "C4999", "C6099", "C6799", "C9599", "C9199",
                                        "C7099", "C5099", "C9099", "C3099", "C4899", 
                                        "C4799", "C5599", "C6699", "C6199", "U1111")

COLORS: Tuple[str, ...] = ("#FFC300", "#FF5733", "#C70039", "#900C3F", "#5C6D70",
                           "#2C2C54", "#5FAD56", "#F2C14E", "#F78154", "#4D9078",
                           "#4A1942", "#823329", "#3F7CAC", "#899878", "#5497A7", 
                           "#883677", "#3A7D44", "#254D32", "#F7CE5B", "#F7B05B")

DEL_COLUMNS: List[str]= ["ficdep", "fictra", "artipo", "ficpro", 
                         "pronom", "ficrem", "ficfac", "corte", 
                         "signo", "transfe", "ficmov"]

# Paths
MAIN_PATH: Path = Path().cwd()
OUT_PATH: str = f"{Path.home()}/Documents/Programas/auto_plot/out"
TEST_PATH: str = f"{MAIN_PATH}/src/views/test"
DB_PATH: str = f"{MAIN_PATH}/src/db/indices.db"
JSON_PATH: str = f"{MAIN_PATH}/src/data/json_data"

# Dates
TODAY_DATE_PAGE = pd.Timestamp.today().strftime("%d/%m/%Y")
TODAY_DATE_FILE = pd.Timestamp.today().strftime("%d-%m-%Y")
TODAY_FOR_DELTA = pd.Timestamp(pd.to_datetime('today').strftime("%Y-%m"))

# Movs
MOV_SALIDAS: str = "Transf al Dep |Salida"
MOV_ENTRADAS: str = "Tranf desde |Transf Recibida|Entrada "
MOV_DEVOLUCIONES: str = "Devolucion"
