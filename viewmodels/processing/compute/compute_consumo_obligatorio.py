from datetime import date

import pandas as pd

from config.enums import ConsumoObligatorioEnum
from viewmodels.common.coches_cabecera_vm import CochesCabeceraVM
from viewmodels.consumo.obligatorio.vm import ConsumoObligatorioVM


def compute_consumo_obligatorio(df: pd.DataFrame, repuesto: ConsumoObligatorioEnum) -> None:
    df_final: pd.DataFrame = pd.DataFrame()
    df_coches_cabecera: pd.DataFrame = CochesCabeceraVM().get_df()

    df_final["Cabecera"] = df["Cabecera"]
    df_final["Repuesto"] = repuesto
    df_final["Año2023"] = df["Año2023"]
    df_final["Año2024"] = df["Año2024"]
    df_final["Año2025"] = df["Año2025"]

    df_final = df_final.merge(
        df_coches_cabecera[["Cabecera", "CochesSinScania"]],
        on="Cabecera",
        how="left",
    )

    df_final["MinimoObligatorio"] = df_final["CochesSinScania"] * 2
    df_final = df_final.drop(columns=["CochesSinScania"])

    df_final["UltimaFecha"] = date.today()

    ConsumoObligatorioVM().save_df(df_final)

