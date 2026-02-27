from enum import auto
from typing import List
from strenum import StrEnum

class PlotlyComponentsColorsEnum(StrEnum):
    TRANSPARENTE    = "rgba(0,0,0,0)"
    BLANCO          = "white"
    BLANCO_RGBA     = "rgba(255,255,255)"
    GRIS            = "gray"
    GRIS_OSCURO     = "#3D4044"
    NEGRO           = "#0E1117"
    ROJO            = "#C70039"
    VERDE           = "#3A7D44"
    AMARILLO        = "#F2C14E"
    VIOLETA         = "#2C2C54"


class TransferEntreDepoColorsEnum(StrEnum):
    ROJO = "#C70039"
    AZUL = "#3F7CAC"


class HistorialColorsEnum(StrEnum):
    VIOLETA = "#4A1942"
    LILA    = "#883677"
    VERDE   = "#5FAD56"


class IndiceColorsEnum(StrEnum):
    CELESTE                 = "#5497A7"
    ROJO                    = "#C70039"
    BORDO                   = "#900C3F"
    GRIS                    = "#5C6D70"
    AZUL_VIOLETA            = "#414770"
    VERDE_AGUA              = "#0C7C59"
    MARRON_OSCURO           = "#823329"
    MORADO                  = "#883677"
    NARANJA                 = "#F78154"
    SALMON                  = "#FE5F55"
    AZUL_OSCURO             = "#0A2342"
    VERDE_AGUA_CLARO        = "#2CA58D"
    VIOLETA                 = "#502F4C"
    LILA                    = "#9C88AC"
    VERDE_AGUA_OSCURO       = "#225560"
    BEIGE                   = "#E39774"
    VERDE_MANZANA           = "#698F3F"
    MARRON_MEDIO            = "#804E49"
    LADRILLO                = "#B0413E"
    VERDE_OSCURO            = "#226F54"
    ROJO_BORDO              = "#A4031F"
    GRIS_CLARO              = "#7D8491"
    NARANJA_OSCURO          = "#FF5733"
    AMARILLO                = "#F2C14E"
    VERDE_AGUA_INTERMEDIO   = "#4D9078"
    GRIS_VERDOSO            = "#828E82"
    BLANCO_VERDOSO          = "#BAC1B8"

    @classmethod
    def as_list(cls) -> List[str]:
        return [color.value for color in cls]


class HoverColorsEnum(StrEnum):
    NEGRO   = "#0E1117"
    VIOLETA = "#833E73"


class FallaGarantiasColorsEnum(StrEnum):
    AMARILLO    = "#F1D764"
    NARANJA     = "#F4A259"
    VERDE       = "#4D9078"
    ROJO        = "#BC4B51"
    VIOLETA     = "#897AEA"

    @classmethod
    def as_list(cls) -> List[str]:
        return [color.value for color in cls]


class ConsumoGarantiasColorsEnum(StrEnum):
    ROJO    = "#C70039"
    VERDE   = "#0C7C59"


class ConsumoObligatorioColorsEnum(StrEnum):
    NARANJA_OSCURO  = "#FF5733"
    AMARILLO        = "#FFC300"
    NARANJA         = "#F78154"
    AZUL            = "#5497A7"
    VERDE           = "#4D9078"


class DuracionRepuestosColorsEnum(StrEnum):
    NARANJA         = "#FE7F2D"
    AZUL            = "#4C8DB4"
    VIOLETA         = "#806FA3"
    VERDE_OSCURO    = "#619B8A"
    VERDE_CLARO     = "#A1C181"
    AMARILLO        = "#FCCA46"

    @classmethod
    def as_list(cls) -> List[str]:
        return [color.value for color in cls]


class ConsumoComparacionOscuroColorsEnum(StrEnum):
    NARANJA         = "#B35516"
    AZUL            = "#146EA7"
    VIOLETA         = "#6841B6"
    VERDE_OSCURO    = "#249372"
    VERDE_CLARO     = "#64A029"
    AMARILLO        = "#D2A017"

    @classmethod
    def as_list(cls) -> List[str]:
        return [color.value for color in cls]


class PrevisionColorsEnum(StrEnum):
    LILA            = "#883677"
    VIOLETA         = "#485696"
    NARANJA         = "#F24C00"
    NARANJA_FUERTE  = "#FF5733"


class CustomMetricColorsEnum(StrEnum):
    VERDE       = "#5B8E7D"
    ROJO        = "#BC4B51"
    AZUL        = "#4C8DB4"
    AMARILLO    = "#F1D764"
    VIOLETA     = "#806FA3"
    NARANJA     = "#F78154"

    @classmethod
    def as_list(cls) -> List[str]:
        return [color.value for color in cls]


class ColoresMatplotlibEnum(StrEnum):
    YlOrRd  = auto()
    YlGnBu  = auto()
    plasma  = auto()
    viridis = auto()
    magma   = auto()
    PuBuGn  = auto()


# Texto
class ForegroundColorsEnum(StrEnum):
    T_RED           = '\033[91m'
    T_LIGHT_RED     = '\033[31m'
    T_GREEN         = '\033[92m'
    T_LIGHT_GREEN   = '\033[32m'
    T_YELLOW        = '\033[33m'
    T_BLUE          = '\033[94m'
    T_PURPLE        = '\033[95m'
    T_CYAN          = '\033[96m'
    T_WHITE         = '\033[97m'
    T_BLACK         = '\033[90m'
    T_MAGENTA       = '\033[35m'
    T_GRAY          = '\033[90m'
    T_ORANGE        = '\033[38;5;208m'
    T_FUCHSIA       = '\033[38;5;170m'


class BackgroundColorsEnum(StrEnum):
    B_RED       = '\033[41m'
    B_ORANGE    = '\033[48;5;208m'


class TextModsEnum(StrEnum):
    UNDERLINE   = '\033[4m'
    ITALIC      = '\033[3m'
    RESET       = '\033[0m'