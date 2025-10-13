from enum import auto, Enum
from strenum import UppercaseStrEnum, StrEnum, PascalCaseStrEnum

from src.config.dataclasses import Cabeceras


class WithZeroEnum(UppercaseStrEnum):
    ZERO = auto()
    NON_ZERO = auto()


class IndexTypeEnum(UppercaseStrEnum):
    VEHICULO = auto()
    MOTOR = auto()


class ScrapEnum(UppercaseStrEnum):
    WEB = auto()
    LOCAL = auto()


class CabecerasEnum(PascalCaseStrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ")

    POMPEYA = auto()
    LA_NORIA = auto()
    BONZI = auto()
    EVA_PERON = auto()
    MEDINA = auto()
    CUSA = auto()
    ETAPSA = auto()
    LUJAN = auto()
    MASCHWITZ = auto()
    BARRACAS = auto()
    PILAR = auto()
    CONSTITUYENTES = auto()
    SAN_VICENTE = auto()
    LONGCHAMPS = auto()
    TG_LANUS = auto()
    TG_CALZADA = auto()
    TG_CIUDADELA = auto()
    TARSA_LANUS = auto()
    TARSA_134 = auto()
    SAN_ISIDRO = auto()
    MEGABUS_EJERCITO = auto()
    EL_PUENTE = auto()


class RepuestoEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ").upper()

    INYECTOR = auto()
    BURRO = auto()
    ALTERNADOR = auto()
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
    UREA = auto()
    CINTAS_FRENO = auto()
    PASTILLAS_FRENO = auto()


class LoadDataEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ").capitalize()

    INDICES_DE_CONSUMO = auto()
    PREVISION_DE_CONSUMO = auto()
    DESVIACION_DE_INDICES = auto()
    DATOS_GARANTIAS = auto()
    FALLA_GARANTIAS = auto()
    CONSUMO_GARANTIAS = auto()
    MAXMIMOS_Y_MINIMOS = auto()


class CabecerasCompletasEnum(Enum):
    POMPEYA = Cabeceras("Pompeya", "POMPEYA")
    LA_NORIA = Cabeceras("La Noria", "LA NORIA")
    BONZI = Cabeceras("Bonzi", "BONZI")
    EVA_PERON = Cabeceras("Eva Perón", "EVA PERON")
    MEDINA = Cabeceras("Medina", "MEDINA")
    CUSA = Cabeceras("Cusa","CUSA")
    ETAPSA = Cabeceras("Etapsa", "ETAPSA")
    LUJAN = Cabeceras("Luján", "LUJAN")
    MASCHWITZ = Cabeceras("Maschwitz", "MASCHWITZ")
    BARRACAS = Cabeceras("Barracas", "BARRACAS")
    PILAR = Cabeceras("Pilar", "PILAR")
    CONSTITUYENTES = Cabeceras("Constituyentes", "CONSTITUYENTES")
    SAN_VICENTE = Cabeceras("San Vicente", "SAN VICENTE")
    LONGCHAMPS = Cabeceras("Longchamps", "LONGCHAMPS")
    TG_LANUS = Cabeceras("TG Lanús", "TG LANUS")
    TG_CALZADA = Cabeceras("TG Calzada", "TG CALZADA")
    TG_CIUDADELA = Cabeceras("TG Ciudadela", "TG CIUDADELA")
    TARSA_LANUS = Cabeceras("Tarsa Lanus", "TARSA 100")
    TARSA_134 = Cabeceras("Tarsa 134", "TARSA 134")
    SAN_ISIDRO = Cabeceras("San Isidro", "SAN ISIDRO")
    MEGABUS_EJERCITO = Cabeceras("Megabus Ejercito", "MEGABUS EJERCITO")
    EL_PUENTE = Cabeceras("El Puente", "EL PUENTE")