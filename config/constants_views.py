from typing import Tuple

MAIN_TABS: Tuple[str, ...] = (" 🏠 Página principal", " 📊 Índices de consumo",
                              " 📈 Previsión de consumo", " 📊 Desviación de índices",
                              " 🚫 Falla Garantías", " ↕️ Máximos y Mínimos")


# Pags Inicio
PAG_PRINCIPAL = "Página principal 🏠"
PAG_SISSSA = "SISSSA FLOTA"
PAG_DOTA_LICITACIONES = "DOTA LICITACIONES"
PAG_CARGAR_DATOS = "Cargar datos 🔄️"
PAG_NUEVO_USUARIO = "Nuevo usuario 👤"

# Pags Consumo
PAG_INDICES = "Índices de consumo 📊"
PAG_HISTORIAL = "Historial de consumos 💽"
PAG_CONSUMO_OBLIGATORIO = "Consumo Obligatorio 🚨"
PAG_PREVISION = "Previsión de consumo 📈"
PAG_DESVIACION_INDICES = "Desviaciones de índices 📊"
PAG_DURACION = "Duracion de repuestos 🛠️"
PAG_COMPARACION_CONSUMO = "Comparación de consumo 🧩"

# Pags Garantias
PAG_FALLA_GARANTIAS = "Falla equipos garantías ⛔"

# Pags info.
PAG_MAXIMOS_MINIMOS = "Máximos y Mínimos ⬆️⬇️"
PAG_COCHES_CABECERA = "Coches por cabecera 🚌"
PAG_PARQUE_MOVIL = "Parque Móvil 🚌🚏"

# Pags Gomeria
PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS = "Transferencias entre depósitos 🔃"

# Tabs
TABS_FALLAS = ("🚫 Falla Equipos Garantías", "📊 Consumos Garantias y Transferencias")
TABS_DURACION = ("🛠️ General", "🔧 Por repuesto")

# Selectboxes
PLACEHOLDER = "------"


# HTML
HTML_SIN_CAMBIOS = """<p style='
                    color: #F1D764; 
                    font: bold light 18px sans-serif;
                    background: #0E1117; 
                    border-radius: 5px;
                    border-width: 2px;
                    border-style: solid; 
                    border-color: #3D4044;
                    text-align: center'>"""

# CSS
CSS_CONTEO = """
            <style>
            [data-testid="stMetricValue"] {
                font-size: 32px;
                color: #4CAF50;
            }
            
            [data-testid="stMetricDelta"] {
                color: #00c853;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 14px;
                color: #FFFFF;
            }
            </style>
             """


# HEIGHT
PIE_PLOT_HEIGHT                 : int = 585
DATAFRAME_HEIGHT                : int = 600
LINK_BOX_HEIGHT                 : int = 72
SELECT_BOX_HEIGHT               : int = 120
MULTI_SELECT_BOX_HEIGHT         : int = 150
CENTERED_TITLE_HEIGHT           : int = 78
BARPLOT_BOX_HEIGHT              : int = 700
PLOT_BOX_HEIGHT                 : int = 535
PIE_PLOT_BOX_HEIGHT             : int = 700
CONTEO_BOX_HEIGHT               : int = 700
CONTEO_STATS_HEIGHT             : int = 200
MULTIPLE_PLOT_BOX_HEIGHT        : int = 700
FULL_PLOT_BOX_HEIGHT            : int = 650
FULL_PLOT_BOX_TRANSFER_HEIGHT   : int = 955
TEXT_BOX_HEIGHT                 : int = 450
TAB_BOX_HEIGHT                  : int = 770
DURACION_TAB_BOX_HEIGHT         : int = 880
DESVIACION_BOX_HEIGHT           : int = 818
FILE_UPLOADER_HEIGHT            : int = 368
FALLA_TAB_BOX_HEIGHT            : int = 870
FALLA_GARANTIAS_BOX_HEIGHT      : int = 700
FLOTA_CONTAINER_HEIGHT          : int = 100
GOMERIA_DIFERENCIA_BOX_HEIGHT   : int = 737
GOMERIA_TRANSFER_BOX_HEIGHT     : int = 601
CARGAR_DATOS_BASIC_HEIGHT       : int = 335
CARGAR_DATOS_MULTI_HEIGHT       : int = 470
INPUT_HEIGHT                    : int = 100
NUEVO_USUARIO_RADIO_HEIGHT      : int = 170


# WIDTH
PIE_PLOT_WIDTH          : int = 585
BARPLOT_WIDTH           : int = 1100
LINK_BOX_WIDTH          : int = 350
SELECT_BOX_WIDTH        : int = 650
CENTERED_TITLE_WIDTH    : int = 570
BARPLOT_BOX_WIDTH       : int = 1600
PIE_PLOT_BOX_WIDTH      : int = 1550


# FONT
PIE_FONT_SIZE: int = 24


# DISTANCE
DISTANCE_COLS_SELECT_PLOT   : Tuple[int, int] = (1, 5)
DISTANCE_COLS_DUAL_PLOT     : Tuple[int, float] = (1, 1.8)
DISTANTE_COLS_DUAL_SELECT   : Tuple[int, float] = (1, 0.5)

DISTANCE_COLS_SELECTBIGGER_PLOT : Tuple[float, int] = (0.70, 3)
DISTANCE_COLS_CENTER_TITLE      : Tuple[float, int, int] = (0.95, 3, 1)
