from typing import Tuple

import pandas as pd

from config.constants_common import CONSUMO_COMPARACION_COLS_TYPE, CONSUMO_COMPARACION_COLS, CONSUMO_COMPARACION_COLS_RENAME
from config.enums import ConsumoComparacionRepuestoEnum, PeriodoComparacionEnum
from viewmodels.consumo_vm import ConsumoComparacionVM
from viewmodels.datos_vm import JSONConfigVM


def compute_comparacion_consumo(df: pd.DataFrame, tipo_rep: ConsumoComparacionRepuestoEnum) -> None:
    if df.empty:
        return None

    df: pd.DataFrame = df.copy()[CONSUMO_COMPARACION_COLS]
    df = df.rename(columns=CONSUMO_COMPARACION_COLS_RENAME) # type: ignore
    df.insert(3, "TipoRepuesto", tipo_rep)

    df["Cabecera"] = df["Cabecera"].str[-2:].str.strip()
    df["Cabecera"] = df["Cabecera"].map(JSONConfigVM().get_df_by_name("transferencias"))

    df["FechaCompleta"] = pd.to_datetime(df["FechaCompleta"], dayfirst=True, format='mixed')

    fecha_min = df["FechaCompleta"].min()
    fecha_max = df["FechaCompleta"].max()

    periodo = None

    if fecha_max.year in (fecha_min.year, fecha_min.year + 1):
        periodo = next((p for p in PeriodoComparacionEnum if p.numero == fecha_min.year), None)

    df["FechaTitulo"]   = f"({fecha_min.date()} | {fecha_max.date()})"
    df["PeriodoID"]     = periodo

    df = pd.DataFrame(df.astype(CONSUMO_COMPARACION_COLS_TYPE))

    df["Consumo"]   = df["Consumo"].str.replace(",", ".").astype("float64").round(1)
    df["Gasto"]     = df["Gasto"].str.replace(",", ".").astype("float64").round(1)

    ConsumoComparacionVM().save(df)
    return None
