from enum import auto
from typing import List

from strenum import UppercaseStrEnum, StrEnum, PascalCaseStrEnum, LowercaseStrEnum


class TipoCargarEnum(PascalCaseStrEnum):
    UNICO = auto()
    MULTIPLE = auto()


class IndexTypeEnum(UppercaseStrEnum):
    VEHICULO = auto()
    MOTOR = auto()


class MovimientoEnum(UppercaseStrEnum):
    SALIDAS = auto()
    ENTRADAS = auto()
    DEVOLUCIONES = auto()
    TRANSFERENCIAS = auto()

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
    ESISA = auto()
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
    MEGABUS_EJERCITO = auto()
    EL_PUENTE = auto()


class TendenciaEnum(PascalCaseStrEnum):
    LINEAL = auto()
    CUADRATICA = "Cuadrática"
    CUBICA = "Cúbica"


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
    REFRIGERANTE = auto()
    ACEITE_DE_MOTOR = auto()
    ACEITE_DE_CAJA = auto()
    ACEITE_DE_DIFERENCIAL = auto()
    GRASA_DE_DIFERENCIAL = auto()
    CINTAS_FRENO_1 = auto()
    CINTAS_FRENO_2 = auto()
    PASTILLAS_FRENO = auto()
    BANANAS = auto()
    PULMON_SUSPENSION = auto()
    MOTOR_CONDENSADOR = auto()
    BITURBO = auto()
    FILTRO_AIRE_ACONDICIONADO = auto()


class RepuestoReparadoEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ").upper()

    CAJA_AUTOMATICA_REP_T270 = auto()
    RETEN_RUEDA_EJE_CENTRAL_MT27_EXTERIOR = auto()
    RETEN_RUEDA_EJE_CENTRAL_MT27_INTERIOR = auto()
    RULEMAN_RUEDA_EJE_CENTRAL_MT27 = auto()
    MAZA_RUEDA_EJE_CENTRAL_MT27 = auto()


class TipoDuracionEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ").upper()

    CAJAS_REPARADAS = auto()
    RETEN = auto()
    RULEMAN = auto()
    MAZA = auto()


class ConsumoObligatorioEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ").upper()

    FILTRO_SECADOR_GOBERNADOR_APU_TB1394_16X = auto()


class ConsumoComparacionRepuestoEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ").upper()

    COMPRESOR   = auto()
    GAS         = auto()


class PeriodoComparacionEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ").upper()

    @classmethod
    def as_list(cls) -> List[str]:
        return [periodo.value for periodo in cls]

    DESDE_2020_A_2021 = auto()
    DESDE_2021_A_2022 = auto()
    DESDE_2022_A_2023 = auto()
    DESDE_2023_A_2024 = auto()
    DESDE_2024_A_2025 = auto()
    DESDE_2025_A_2026 = auto()




class LoadDataEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ").capitalize()

    USUARIO                                 = auto()
    INDICES_DE_CONSUMO                      = auto()
    PREVISION_DE_CONSUMO                    = auto()
    HISTORIAL_CONSUMO                       = auto()
    CONSUMO_OBLIGATORIO                     = auto()
    FALLA_GARANTIAS                         = auto()
    CONSUMO_GARANTIAS                       = auto()
    MAXIMOS_Y_MINIMOS                       = auto()
    DURACION_REPUESTOS                      = auto()
    TRANSFERENCIAS_ENTRE_DEPOSITOS          = auto()
    DIFERENCIA_MOVIMIENTOS_ENTRE_DEPOSITOS  = auto()
    PARQUE_MOVIL                            = auto()
    CONTEO_STOCK                            = auto()
    COMPARACION_CONSUMO                     = auto()


class SymbolEnum(LowercaseStrEnum):
    X               = auto()
    CIRCLE          = auto()
    SQUARE          = auto()
    LINE_EW_OPEN    = "line-ew-open"


class DashEnum(LowercaseStrEnum):
    SOLID   = auto()
    DOT     = auto()
    DASH    = auto()


class RoleEnum(LowercaseStrEnum):
    ADMIN = auto()
    USER = auto()