from enum import auto
from strenum import UppercaseStrEnum, PascalSnakeCaseStrEnum 

class WithZeroEnum(UppercaseStrEnum):
    ZERO = auto()
    NON_ZERO = auto()

class IndexTypeEnum(UppercaseStrEnum):
    VEHICULO = auto()
    MOTOR = auto()

class ScrapEnum(UppercaseStrEnum):
    WEB = auto()
    LOCAL = auto()

class RepuestoEnum(PascalSnakeCaseStrEnum):
    INYECTOR = auto()
    BOMBA_UREA = auto()
    CALIPER = auto()
    ELECTROVALVULA = auto()
    FLOTANTE_GASOIL = auto()
    RETEN = auto()
    SENSOR = auto()
    TALADRO = auto()
    BOMBA_INYECTORA = auto()
    CAMARA = auto()
    DVR = auto()
    HERRAMIENTA = auto()