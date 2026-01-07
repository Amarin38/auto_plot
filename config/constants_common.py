from pathlib import Path
from pandas import Timestamp

# PATHS
MAIN_PATH = Path().cwd()
RESOURCES_PATH = "resources/"
IMG_PATH = f"{RESOURCES_PATH}images/"
JSON_PATH: str = f"{MAIN_PATH}/data/json_data"
COMMON_DB_PATH: str = f"{MAIN_PATH}/infrastructure/db/common_data.db"
SERV_DB_PATH: str = f"{MAIN_PATH}/infrastructure/db/services_data.db"
DB_PATH: str = f"sqlite:///{MAIN_PATH}/infrastructure/db/data.db"

# PAGINAS
FLOTA_URL = "https://sistemasanantonio.com.ar/san_antonio/mod_flota/Grilla_ParqueMovil.aspx"
LICITACIONES_URL = "https://dota.sistemasanantonio.com.ar/licitaciones/login.aspx"

# DATES
PAGE_STRFTIME_DMY = "%d/%m/%Y"
PAGE_STRFTIME_YMD = "%Y/%m/%d"
FILE_STRFTIME_DMY = "%d-%m-%Y"
FILE_STRFTIME_YMD = "%Y-%m-%d"
DELTA_STRFTIME_YM = "%Y-%m"
DELTA_STRFTIME_MY = "%m-%Y"
NORMAL_DATE_YMD = "YYYY-MM-DD"

TODAY_DATE_PAGE = Timestamp.today().strftime(PAGE_STRFTIME_DMY)
TODAY_DATE_FILE_DMY = Timestamp.today().strftime(FILE_STRFTIME_DMY)
TODAY_DATE_FILE_YMD = Timestamp.today().strftime(FILE_STRFTIME_YMD)
TODAY_FOR_DELTA = Timestamp.today().strftime(DELTA_STRFTIME_YM)

# Plots
TITULOS_GOMERIA = ("Consumos", "", "Costos", "", "Diferencias consumos", "", "Diferencias costos")
ANCHO_COLS_GOMERIA = (0.30, 0.15, 0.30, 0.20, 0.20, 0.15, 0.20)
TICK_VALS_GOMERIA = ("2024", "2025", "DiferenciaConsumos", "DiferenciaCostos")
TICK_TEXT_GOMERIA = ("Año 2024", "Año 2025", "Diferencia Consumos", "Diferencia Costos")


MODELOS_CHASIS = ("MT 12","MT 13","MT 15","MT 17","MT 17 BOOGIE","MT 27"
        ,"MA 10","MA 15","MA 15" ,"MA 17","MA 27","1114","1115"
        ,"1315","1316","1320","1418","1618","1621","1718","1720"
        ,"1722","13000","1114/48","1114/51","1320/51","1618/52"
        ,"22-A-10000","88-14000","BMO 368 1618 L 55CA","BU1115E"
        ,"D12","D12M","FORD TRANSIT 2.2 L 350L TE","FURGOVAN"
        ,"HIACE","J6LZ1","K250 B4X2","K280B","K310 A6X2","KANGOO"
        ,"L312/48","MASTER","MTF BU","MTT BU","O500","OA101"
        ,"OA101","OA101/5","OA105","OF1417","OF1418","OF1722"
        ,"OH1315","OH1316","OH1320","OH1321","OH1323","OH1324"
        ,"OH1420","OH1618","OH1621","OH1621" ,"OH1721","OH1721LSB"
        ,"OH1816","OHL1320","OHL1320/51","OHL1420","OHL1420/60"
        ,"OHL1621","OHL1621/52","OHL1721LSB","T112H4X","TONY")

MARCAS_CHASIS = ("AGRALE","CHASISNUEVO","CHEVROLET","DETALLE"
                ,"MATERFER","MBENZ","METALPAR","PUMA"
                ,"RENAULT","SCANIA","SPRINTER","TOYOTA")

MODELOS_MOTOR = ("CUMMINS 4C","CUMMINS 6C","MAXXFORCE 4C","MAXXFORCE 6C","MWM 4C"
                ,"SCANIA 6C","WEICHAI","DC 09 142 280CV","HTM3500","MBENZ", "ISB 6.7 286 P7")

MARCAS_MOTOR = ("CUMMINS","MWM","EQUIPMAKE","MBENZ","SCANIA","WEICHAI")

CARROCERIAS = ("25 DE MAYO","AGRALE","AGUATEROLONGH","AGUILA","ALASA"
              ,"AUTOBOMBA","AUTOBUS","AUXILIO","BAM BAM","BEDFORD"
              ,"CAMION","CON PALA","CORWIN","DESGUACE","EIVAR"
              ,"EL DETALLE","ELVIO","EVA PERON","FORD","FURGON"
              ,"GALICIA","INSTITUCIONAL","ITALBUS","LA FAVORITA"
              ,"LANUS","LUJAN","MARCOLA","MARCOPOLO","MATERFER"
              ,"MBENZ","METALBUS","METALPAR","METALSUR","MONTANA",
               "MULETO","MURABITO","NITRAMOTOR","NO VENDER"
              ,"NUOVOBUS","OTTAVIANO","PEVERI","POMPEY","PUMA DE TAT","QUEMADO"
              ,"REPUESTOS","SALDIVIA","SAN JUAN","SAN MIGUEL","SANCHEZ"
              ,"SCANIA","SOLDATI","SPLENDID","TATSA","TODOBUS"
              ,"TURISMO","UGARTE","VAPOR","VENDIDO","VW GOL")

