import pandas as pd

from src.db_data.crud_services import df_to_db

def calcular_consumo_garantias(df: pd.DataFrame) -> None:
    df_garantias = df.loc[df["Tipo"] == "GARANTIA"]
    df_garantias = (df_garantias.groupby(["Cabecera","Tipo"])
                    .agg({"Cantidad":"sum"})
                    .rename(columns={"Cantidad":"Garantia"})
                    .reset_index())

    df_transferencias = df.loc[df["Tipo"] == "TRANSFERENCIA"]
    df_transferencias = (df_transferencias.groupby(["Cabecera","Tipo"])
                         .agg({"Cantidad": "sum"})
                         .rename(columns={"Cantidad": "Transferencia"})
                         .reset_index())

    df_final = pd.concat([df_garantias, df_transferencias])
    df_final["Total"] = df_final["Garantia"] + df_final["Transferencia"]

    df_to_db('consumo_garantias', df_final)


def calcular_falla_garantias(df: pd.DataFrame) -> None:
    df = (df.groupby(["Cabecera", "Repuesto"])
          .agg({"DiasColocado":"mean"})
          .rename(columns={"DiasColocado":"PromedioTiempoFalla"})
          .reset_index())

    df_to_db('falla_garantias', df)


def guardar_datos_garantias(df: pd.DataFrame) -> None:
    df_to_db('datos_garantias', df)