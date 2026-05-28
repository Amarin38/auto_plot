from pathlib import Path
from typing import List

from pandas import Timestamp

# PATHS
MAIN_PATH = Path().cwd()
RESOURCES_PATH  : str = "resources/"
IMG_PATH        : str = f"{RESOURCES_PATH}images/"
JSON_PATH       : str = f"{MAIN_PATH}/data/json_data"
COMMON_DB_PATH  : str = f"{MAIN_PATH}/infrastructure/db/common_data.db"
SERV_DB_PATH    : str = f"{MAIN_PATH}/infrastructure/db/services_data.db"
DB_PATH         : str = f"sqlite:///{MAIN_PATH}/infrastructure/db/data.db"

# PAGINAS
FLOTA_URL               = "https://sistemasanantonio.com.ar/san_antonio/mod_flota/Grilla_ParqueMovil.aspx"
LICITACIONES_URL        = "https://dota.sistemasanantonio.com.ar/licitaciones/login.aspx"


# GOOGLE SHEETS
PROVEEDORES_SHEET_URL   = "https://docs.google.com/spreadsheets/d/1pm3sEx1Ww1rkn4fJaulICRsH2BRvQmAqwDp4rNACmKA/edit?gid=1467417956#gid=1467417956"
PREVISION_SHEET_URL     = "https://docs.google.com/spreadsheets/d/1v98qsIyWfvvk5jCEPSZ9FiCggv9clf8OdQk_33bUm_0/edit?gid=0#gid=0"
MAX_MIN_SHEET_URL       = "https://docs.google.com/spreadsheets/d/1LKY8enH8MzIuQexQsih2LwHVe2pSGX4mkJMWZC1oKcE/edit?gid=0#gid=0"

# WORKSHEETS
PROVEEDORES_WS          = "Hoja 1"


# SESSION KEYS
INDEX = "_index_prev"

PROVEEDORES_DF_KEY = "proveedores_df"
PROVEEDORES_PAGER_KEY = "proveedores_pager"
PROVEEDORES_EDITOR_KEY = "proveedores_editor"

PREVISION_DF_KEY = "prevision_df"
PREVISION_EDITOR_KEY = "prevision_editor"
PREVISION_STOCK_EDITOR_KEY = "prevision_stock_editor"
PREVISION_REPUESTO_KEY = "prevision_repuesto"
PREVISION_ULTIMO_REPUESTO_KEY = "ULTIMO_REPUESTO"
PREVISION_DF_STOCK_KEY = "df_stock"
PREVISION_DF_CONSUMO_KEY = "df_consumo"

COMPARACION_CABECERA_KEY = "CABECERA_COMPARACION"
COMPARACION_TIPO_REP_KEY = "REP_COMPARACION"
COMPARACION_PERIODO_KEY = "PERIODO"

DURACION_REPUESTO_KEY = "DURACION_REPUESTO_GENERAL"

MAX_MIN_CABECERA_KEY    = "MAX_MIN_CABECERA"
MAX_MIN_DF_KEY          = "MAX_MIN_DF"
MAX_MIN_DF_STOCK_KEY     = "MAX_MIN_DF_DATA"
MAX_MIN_TABLE_KEY       = "MAX_MIN_TABLE"
MAX_MIN_EDITOR_KEY      = "MAX_MIN_EDITOR"
MAX_MIN_PAGER_KEY       = "MAX_MIN_PAGER"
MAX_MIN_DATA_PAGER_KEY   = "MAX_MIN_DATA_PAGER"

# DATES
PAGE_STRFTIME_DMY   = "%d/%m/%Y"
PAGE_STRFTIME_YMD   = "%Y/%m/%d"
FILE_STRFTIME_DMY   = "%d-%m-%Y"
FILE_STRFTIME_YMD   = "%Y-%m-%d"
DELTA_STRFTIME_YM   = "%Y-%m"
DELTA_STRFTIME_MY   = "%m-%Y"
NORMAL_DATE_YMD     = "YYYY-MM-DD"

TODAY_DATE_PAGE     = Timestamp.today().strftime(PAGE_STRFTIME_DMY)
TODAY_DATE_FILE_DMY = Timestamp.today().strftime(FILE_STRFTIME_DMY)
TODAY_DATE_FILE_YMD = Timestamp.today().strftime(FILE_STRFTIME_YMD)
TODAY_FOR_DELTA     = Timestamp.today().strftime(DELTA_STRFTIME_YM)

MESES_ESPAÑOL = {
    1: 'Ene', 2: 'Feb', 3: 'Mar',
    4: 'Abr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Sep',
    10: 'Oct', 11: 'Nov', 12: 'Dic'
}

VACIO_FECHA = "  -   -"


# Filtro
FILTRO_OBS = "0KM|TRANSMISIÓN|CAMBIO"

# MOVS
MOV_SALIDAS         : str = "TRD|DES"
MOV_ENTRADAS        : str = "COM|TRA"
MOV_DEVOLUCIONES    : str = "DEU|DEC"
MOV_TRANSFERENCIAS  : str = "TRD"


# LISTAS DE DATOS
INTERNOS_DEVOLUCION: List[str] = ["C0488", "C0489", "C0500", "C0700", "C1400",
                                  "C4500", "C4900", "C6000", "C6700", "C9500",
                                  "C9100", "C7000", "C5000", "C9000", "C3000",
                                  "C4800", "C4700", "U4000", "C6600", "C6400",
                                  "C0199", "C0599", "C0799", "C1499", "C4599",
                                  "C4999", "C6099", "C6799", "C9599", "C9199",
                                  "C7099", "C5099", "C9099", "C3099", "C4899",
                                  "C4799", "C5599", "C6699", "C6199", "U1111"]

MODELOS_CHASIS = ("MT 12","MT 13","MT 15","MT 17","MT 17 BOOGIE","MT 27","MA 10","MA 15","MA 15" ,"MA 17",
                  "MA 27","1114","1115","1315","1316","1320","1418","1618","1621","1718","1720","1722","13000",
                  "1114/48","1114/51","1320/51","1618/52","22-A-10000","88-14000","BMO 368 1618 L 55CA","BU1115E",
                  "D12","D12M","FORD TRANSIT 2.2 L 350L TE","FURGOVAN","HIACE","J6LZ1","K250 B4X2","K280B",
                  "K310 A6X2","KANGOO","L312/48","MASTER","MTF BU","MTT BU","O500","OA101","OA101","OA101/5",
                  "OA105","OF1417","OF1418","OF1722","OH1315","OH1316","OH1320","OH1321","OH1323","OH1324","OH1420",
                  "OH1618","OH1621","OH1621" ,"OH1721","OH1721LSB","OH1816","OHL1320","OHL1320/51","OHL1420",
                  "OHL1420/60","OHL1621","OHL1621/52","OHL1721LSB","T112H4X","TONY")

MARCAS_CHASIS = ("AGRALE","CHASISNUEVO","CHEVROLET","DETALLE","MATERFER","MBENZ",
                 "METALPAR","PUMA","RENAULT","SCANIA","SPRINTER","TOYOTA")

MODELOS_MOTOR = ("CUMMINS 4C","CUMMINS 6C","MAXXFORCE 4C","MAXXFORCE 6C","MWM 4C",
                 "SCANIA 6C","WEICHAI","DC 09 142 280CV","HTM3500","MBENZ", "ISB 6.7 286 P7")

MARCAS_MOTOR = ("CUMMINS","MWM","EQUIPMAKE","MBENZ","SCANIA","WEICHAI")

CARROCERIAS = ("25 DE MAYO","AGRALE","AGUATEROLONGH","AGUILA","ALASA","AUTOBOMBA","AUTOBUS","AUXILIO","BAM BAM",
               "BEDFORD","CAMION","CON PALA","CORWIN","DESGUACE","EIVAR","EL DETALLE","ELVIO","EVA PERON","FORD",
               "FURGON","GALICIA","INSTITUCIONAL","ITALBUS","LA FAVORITA","LANUS","LUJAN","MARCOLA","MARCOPOLO",
               "MATERFER","MBENZ","METALBUS","METALPAR","METALSUR","MONTANA" ,"MULETO","MURABITO","NITRAMOTOR",
               "NO VENDER","NUOVOBUS","OTTAVIANO","PEVERI","POMPEY","PUMA DE TAT","QUEMADO","REPUESTOS","SALDIVIA",
               "SAN JUAN","SAN MIGUEL","SANCHEZ","SCANIA","SOLDATI","SPLENDID","TATSA","TODOBUS","TURISMO","UGARTE",
               "VAPOR","VENDIDO","VW GOL")

DEPOSITOS = ("OFICINA", "FLAVIO")

DESVIACIONES_CHOICES = ("Encima", "Muy por encima", "Igual", "Debajo", "Muy por debajo")

LOC_PROVEEDORES = ("CAP. FED.", "BANFIELD", "VILLA LYNCH", "LANUS", "DOCK SUD", "LANUS ESTE", "TIGRE", "LOMA HERMOSA",
                   "LLAVALLOL", "OLIVOS", "LANUS OESTE", "AVELLANEDA", "SAN JUSTO", "VILLA MADERO", "VILLA INSUPERABLE",
                   "CASTELAR", "VALENTIN ALSINA", "ADROGUE", "SAN FERNANDO", "LA TABLADA", "C.P. 1754",
                   "TEMPERLEY", "MUNRO", "ROSARIO (SANTA FE)", "CABA", "BERNAL", "CIUDAD MADERO", "HAEDO", "MORENO",
                   "LOMAS DEL MIRADOR", "HURLINGHAM", "LUIS GUILLON", "VILLA LUGANO", "SAENZ PEÑA", "ENSENADA",
                   "MONTE GRANDE", "CIUDADELA", "RAMOS MEJIA", "CIUDAD EVITA", "LOMAS DE ZAMORA", "FLORIDA",
                   "JOSE LEON SUAREZ", "SANTOS LUGARES", "VILLA LUZURIAGA", "BOULOGNE", "VILLA MARTELLI", "TABLADA",
                   "JOSE MARMOL", "QUILMES", "VILLA BALLESTER", "MORON", "CAMPANA", "LA PLATA", "FLORIDA 437",
                   "SARANDI", "ISIDRO CASANOVA", "JOSE INGENIEROS", "SAN ISIDRO", "EZEIZA", "LAFERRERE",
                   "R. DE ESCALADA", "ESTEBAN ECHEVERRIA", "PONTEVEDRA", "BRANDSEN", "MALVINAS ARGENTINAS",
                   "SAN MARTIN", "LONGCHAMPS", "GONZALEZ CATAN", "VILLA DOMINICO", "BUENOS AIRES",
                   "SAN MIGUEL", "VIRREY DEL PINO", "ITUZAINGO", "CLAYPOLE", "GRAND BOURG", "MERLO", "BELLA VISTA",
                   "DON BOSCO", "VILLA DE MAYO", "MAR DEL PLATA", "EL TALAR", "BERAZATEGUI", "LOS POLVORINES",
                   "CORDOBA", "MONTE CHINGOLO", "EL PALOMAR", "RAFAEL CASTILLO", "LIBERTAD", "VICENTE LOPEZ",
                   "CANNING", "GARIN", "CASEROS", "TANDIL", "VILLA MAIPU", "BOSQUES", "LUJAN", "DON TORCUATO",
                   "VILLA CELINA", "GRAL. RODRIGUEZ", "BENAVIDEZ", "VILLA BONICH", "TRONCOS DEL TALAR", "CHIVILCOY",
                   "ING. BUDGE (LOMAS)", "EZPELETA", "CIUDADELA SUR", "VILLA ZAGALA", "RANELAGH", "FLORENCIO VARELA",
                   "SANTA FE", "MATADEROS", "VILLA ADELINA", "SAN JUAN", "VICTORIA", "DEL VISO", "SAN PEDRO",
                   "CARLOS SPEGAZZINI", "LA FERRERE", "GENERAL PACHECO", "46121", "BURZACO", "MENDOZA",
                   "SAN LUIS", "MERCEDES", "TOTORAS (SANTA FE)", "PASO DEL REY", "GRAL. PACHECO", "53682234",
                   "RICARDO ROJAS", "BAHIA BLANCA", "ALTA GRACIA", "VILLA FIORITO", "POMPEYA", "MARTIN CORONADO",
                   "SAAVEDRA", "WILDE", "CARAPACHAY", "ING. JUAN ALLAN", "ING. MASCHWITZ", "ESCOBAR", "FLORIDA OESTE",
                   "ENTRE RIOS", "ALDO BONZI", "SAN NICOLAS", "ARECO", "TAPIALES", "SUNCHALES", "AYACUCHO",
                   "GODOY CRUZ MENDOZA", "PASTEUR", "CHACO", "DEL TALAR", "VILLA URQUIZA", "JOSE C. PAZ",
                   "CHINA", "ALVEAR, SANTA FE", "MARTINEZ", "GALVEZ (SANTA FE)", "BALBANERA", "CHACARITA",
                   "VILLA CRESPO", "PILAR", "TOAY (LA PAMPA)", "TORTUGUITAS", "GREGORI DE LAFERRERE",
                   "SANTIAGO DEL ESTERO", "CAÑUELAS", "VILLA DEL PARQUE", "NEUQUEN", "COMODORO RIVADAVIA",
                   "LA REJA", "TRELEW", "VILLA SARMIENTO", "BERNAL OESTE", "FLORES", "LA MATANZA", "PIÑEYRO",
                   "VILLA BOSCH", "WILLIAMS MORRIS", "CIUDAD CORDOBA NORTE", "GONNET, LA PLATA", "BOEDO",
                   "GRAL. GUTIERREZ", "SAN FRANCISCO", "MENDIOLAZA (CORDOBA)", "MAGGIOLO (SANTA FE)",
                   "ABASTO, LA PLATA", "RICARDONE (SANTA FE)", "RAFAELA (SANTA FE)", "VENADO TUERTO (SANTA FE)",
                   "CORONEL DORREGO", "SAN ANDRES", "ZARATE")

# GROUPBY
GROUPBY_CAB_REP = ["Cabecera", "Repuesto"]


# COLUMNAS 
PARQUE_MOVIL_COLS           = ("id", "FechaParqueMovil", "Linea", "Interno", "Dominio", "Asientos",
                               "Año", "ChasisMarca", "ChasisModelo", "ChasisNum", "MotorMarca",
                               "MotorModelo", "MotorNum", "Carroceria")
CONSUMO_COMPARACION_COLS    = ("Familia", "Articulo", "Repuesto", "movnom",
                               "Cantidad", "Precio", "FechaCompleta")
CONSUMO_INDICE_COLS         = ('Cabecera', 'Repuesto', 'TotalConsumo', 'TotalCoste', 'ConsumoIndice')
CONSUMO_HISTORIAL_COLS      = ("Repuesto", "FechaCompleta", "Cantidad")
CONSUMO_GARANTIAS_COLS      = ("Cabecera", "Repuesto", "Garantia", "Transferencia")

PREVISION_COLS              = ["Mes", "Articulo", "ConsumoMensual", "TipoRepuesto"]
PREVISION_STOCK_COLS        = ["FechaStock", "RepuestoStock", "StockActual"]
PREVISION_FORECAST_COLS     = ["FechaPrevision", "Prevision", "RestoStock", "RepuestoPrevision", "TipoRepuestoPrevision"]
PREVISION_LOCAL_COLS: List[str] = ["Repuesto", "TipoRepuesto", "FechaCompleta",
                                   "Año", "Mes", "Tendencia", "TendenciaEstacional"]

MAX_MIN_STOCK_COLS           = ["FamiliaStock", "ArticuloStock", "DescripcionStock", "CabeceraStock", "FechaStock", "Stock"]
MAX_MIN_SHEET_COLS           = ["Familia", "Articulo", "Descripcion", "Cabecera", "Fecha", "Minimo", "Maximo"]


PREVISION_LOCAL_DATA_COLS: List[str] = ["Repuesto", "TipoRepuesto", "FechaCompleta", "Año", "Mes",
                                        "TotalAño", "TotalMes", "Promedio", "IndiceAnual", "IndiceEstacional"]

PROVEEDORES_COLS            = ["NroProv", "RazonSocial", "CUIT", "Localidad", "Mail", "Telefono"]
REPUESTOS_CODIGOS_COLS      = ("Descripcion", "Deposito", "Familia", "Articulo", "Codigos", "CodigosConCero")

DEL_COLUMNS_MOVNOM: List[str] = ["artipo", "ficdep", "fictra", "movnom", "ficpro", "pronom",
                                 "ficrem", "ficfac","corte", "signo", "transfe"]

DEL_COLUMNS_FICMOV: List[str] = ["artipo", "ficdep", "fictra", "ficmov", "ficpro", "pronom",
                                 "ficrem", "ficfac","corte", "signo", "transfe"]



# COLUMNAS TIPO
PARQUE_MOVIL_COLS_TYPE = {
    "Linea": "category",
    "Interno": "uint16",
    "Dominio": "string[pyarrow]",
    "Asientos": "category",
    "Año": "uint16",
    "ChasisMarca": "category",
    "ChasisModelo": "category",
    "ChasisNum": "string[pyarrow]",
    "MotorMarca": "category",
    "MotorModelo": "category",
    "MotorNum": "string[pyarrow]",
    "Carroceria": "category",
}

CONSUMO_COMPARACION_COLS_TYPE = {
    "Familia": "uint16",
    "Articulo": "uint32",
    "Repuesto": "category",
    "TipoRepuesto": "category",
    "Cabecera": str,
    "Consumo": str,
    "Gasto": str,
    "PeriodoID": "category",
    "FechaTitulo": "category"
}

PROVEEDORES_COLS_TYPE = {
    "NroProv": "int64",
    "RazonSocial": str,
    "CUIT": str,
    "Localidad": "category",
    "Mail": str,
    "Telefono": str
}


# COLUMNAS RENAME
CONSUMO_INDICE_COLS_RENAME = {'Cantidad':'TotalConsumo','Precio':'TotalCoste'}
CONSUMO_COMPARACION_COLS_RENAME = {"movnom": "Cabecera", "Cantidad":"Consumo", "Precio": "Gasto"}
CONSUMO_GARANTIAS_COLS_RENAME = {"Cantidad": "Garantia"}
CONSUMO_TRANSFERENCIAS_COLS_RENAME = {"Cantidad": "Transferencia"}
CONSUMO_FALLAS_GARANTIAS_COLS_RENAME = {"DiasColocado": "PromedioTiempoFalla"}
PROVEEDORES_COLS_RENAME = {"Nro prov": "NroProv", "Razon social": "RazonSocial", "Cuit": "CUIT"}
REPUESTOS_CODIGOS_COLS_RENAME = {"Articulo":"Descripcion", "Codigo":"Codigos"}
CONSUMO_DESVIACION_REP_COLS_RENAME = {"ConsumoIndice":"MediaRepuesto"}
CONSUMO_DESVIACION_CAB_COLS_RENAME = {"ConsumoIndice": "MediaCabecera"}
