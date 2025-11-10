import pandas as pd

from utils.exception_utils import execute_safely
from viewmodels.consumo_garantias_vm import ConsumoGarantiasVM
from viewmodels.falla_garantias_vm import FallaGarantiasVM

@execute_safely
def compute_consumo_garantias(df: pd.DataFrame, tipo_repuesto: str) -> None:
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
    df_final.insert(3, "TipoRepuesto", tipo_repuesto)
    df_final["Total"] = df_final["Garantia"] + df_final["Transferencia"]

    resta = df_final["Garantia"] - df_final["Transferencia"]
    df_final["PorcentajeTransferencia"] = abs(round((resta / df_final["Transferencia"]) * 100, 0))
    df_final["PorcentajeGarantia"] = 100 - df_final["PorcentajeTransferencia"]

    # Guardo en la base de datos los porcentajes concatenados con los datos numericos para evitar calcular otra vez
    str_transfer = df_final["Transferencia"].map(int).map(str)
    str_garantia = df_final["Garantia"].map(int).map(str)

    str_porc_transfer = df_final["PorcentajeTransferencia"].map(int).map(str)
    str_porc_garantia = df_final["PorcentajeGarantia"].map(int).map(str)

    df_final["PorcentajeTransferencia"] = f"{str_transfer} ({str_porc_transfer}%)"
    df_final["PorcentajeGarantia"] = f"{str_garantia} ({str_porc_garantia}%)"

    ConsumoGarantiasVM().save_df(df_final)


@execute_safely
def compute_fallas_garantias(df: pd.DataFrame, tipo_repuesto: str) -> None:
    df = df.loc[df["Tipo"] == "GARANTIA"]

    df = (df.groupby(["Cabecera", "Repuesto"])
          .agg({"DiasColocado":"mean"})
          .rename(columns={"DiasColocado":"PromedioTiempoFalla"})
          .reset_index())
    df["PromedioTiempoFalla"] = df["PromedioTiempoFalla"].round(0)

    df.insert(3, "TipoRepuesto", tipo_repuesto)
    FallaGarantiasVM().save_df(df)

