from typing import List

INTERNOS_DEVOLUCION: List[str] = ["C0488", "C0489", "C0500", "C0700", "C1400",
                                  "C4500", "C4900", "C6000", "C6700", "C9500",
                                  "C9100", "C7000", "C5000", "C9000", "C3000",
                                  "C4800", "C4700", "U4000", "C6600", "C6400",
                                  "C0199", "C0599", "C0799", "C1499", "C4599",
                                  "C4999", "C6099", "C6799", "C9599", "C9199",
                                  "C7099", "C5099", "C9099", "C3099", "C4899",
                                  "C4799", "C5599", "C6699", "C6199", "U1111"]

DEL_COLUMNS_MOVNOM: List[str] = ["artipo", "ficdep", "fictra", "movnom", "ficpro", "pronom",
                                 "ficrem", "ficfac","corte", "signo", "transfe"]

DEL_COLUMNS_FICMOV: List[str] = ["artipo", "ficdep", "fictra", "ficmov", "ficpro", "pronom",
                                 "ficrem", "ficfac","corte", "signo", "transfe"]

FORECAST_TREND_COLUMNS: List[str] = ["Repuesto", "TipoRepuesto", "FechaCompleta",
                                     "Año", "Mes", "Tendencia", "TendenciaEstacional"]

FORECAST_DATA_COLUMNS: List[str] = ["Repuesto", "TipoRepuesto", "FechaCompleta", "Año", "Mes",
                                    "TotalAño", "TotalMes", "Promedio", "IndiceAnual", "IndiceEstacional"]

# Filtro
FILTRO_OBS = "0KM|TRANSMISIÓN|CAMBIO"

# MOVS
MOV_SALIDAS: str = "TRD|DES"
MOV_ENTRADAS: str = "COM|TRA"
MOV_DEVOLUCIONES: str = "DEU|DEC"
MOV_TRANSFERENCIAS: str = "TRD"