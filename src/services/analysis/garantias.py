import pandas as pd

from src.db_data.crud_services import df_to_db
from src.utils.exception_utils import execute_safely



@execute_safely
def calcular_consumo_garantias(df: pd.DataFrame) -> None:
    df_garantias = df.loc[df["Tipo"] == "GARANTIA"]
    df_garantias = (df_garantias.groupby(["Cabecera", "Repuesto"])
                    .agg({"Cantidad":"sum"})
                    .rename(columns={"Cantidad":"Garantia"})
                    .reset_index())

    df_transferencias = df.loc[df["Tipo"] == "TRANSFERENCIA"]
    df_transferencias = (df_transferencias.groupby(["Cabecera", "Repuesto"])
                         .agg({"Cantidad": "sum"})
                         .rename(columns={"Cantidad": "Transferencia"})
                         .reset_index())

    df_final = pd.merge(df_garantias, df_transferencias)
    df_final = df_final[["Cabecera", "Repuesto", "Garantia", "Transferencia"]]
    df_final["Total"] = df_final["Garantia"] + df_final["Transferencia"]

    resta = df_final["Garantia"] - df_final["Transferencia"]
    df_final["PorcentajeTransferencia"] = abs(round((resta / df_final["Transferencia"]) * 100, 0))
    df_final["PorcentajeGarantia"] = 100 - df_final["PorcentajeTransferencia"]

    # Guardo en la base de datos los porcentajes concatenados con los datos numericos para evitar calcular otra vez
    df_final["PorcentajeTransferencia"] = df_final["Transferencia"].map(int).map(str) + " (" + df_final["PorcentajeTransferencia"].map(int).map(str) + "%)"
    df_final["PorcentajeGarantia"] = df_final["Garantia"].map(int).map(str) + " (" + df_final["PorcentajeGarantia"].map(int).map(str) + "%)"

    df_to_db('consumo_garantias', df_final)


@execute_safely
def calcular_falla_garantias(df: pd.DataFrame) -> None:
    df = df.loc[df["Tipo"] == "GARANTIA"]

    df = (df.groupby(["Cabecera", "Repuesto"])
          .agg({"DiasColocado":"mean"})
          .rename(columns={"DiasColocado":"PromedioTiempoFalla"})
          .reset_index())
    df["PromedioTiempoFalla"] = df["PromedioTiempoFalla"].round(0)

    df_to_db('falla_garantias', df)

