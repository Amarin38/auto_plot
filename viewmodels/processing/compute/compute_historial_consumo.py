import pandas as pd

from config.enums import RepuestoEnum
from viewmodels.consumo.historial.vm import HistorialConsumoVM


def compute_historial(df: pd.DataFrame, tipo_repuesto: RepuestoEnum) -> None:
    df_historial = df.copy()[["Repuesto", "FechaCompleta", "Cantidad"]]
    df_historial["Año"] = df["FechaCompleta"].dt.year
    df_historial["TipoRepuesto"] = tipo_repuesto

    agrupado = (
        (df_historial.groupby(["TipoRepuesto", "Año"]).agg({"Cantidad":"sum"})
         .rename(columns={"Cantidad":"TotalConsumo"}))
         .reset_index()
    )

    agrupado["FechaMin"] = df_historial["FechaCompleta"].min()
    agrupado["FechaMax"] = df_historial["FechaCompleta"].max()

    print(agrupado)
    HistorialConsumoVM().save_df(agrupado)