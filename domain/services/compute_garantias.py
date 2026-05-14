import pandas as pd

from config.constants_common import CONSUMO_GARANTIAS_COLS_RENAME, CONSUMO_TRANSFERENCIAS_COLS_RENAME, \
    CONSUMO_FALLAS_GARANTIAS_COLS_RENAME, GROUPBY_CAB_REP, CONSUMO_GARANTIAS_COLS
from viewmodels.garantias.falla.vm import FallaGarantiasVM

from utils.exception_utils import execute_safely

fallas = FallaGarantiasVM()

@execute_safely
def compute_consumo_garantias(df: pd.DataFrame, tipo_repuesto: str) -> None:
    df_garantias = group_tipo(df, "GARANTIA", CONSUMO_GARANTIAS_COLS_RENAME)
    df_transferencias = group_tipo(df, "TRANSFERENCIA", CONSUMO_TRANSFERENCIAS_COLS_RENAME)

    df_final = pd.merge(df_garantias, df_transferencias)
    df_final = df_final[CONSUMO_GARANTIAS_COLS]
    df_final.insert(3, "TipoRepuesto", tipo_repuesto)
    df_final["Total"] = df_final["Garantia"] + df_final["Transferencia"]

    resta = df_final["Garantia"] - df_final["Transferencia"]
    df_final["PorcentajeTransferencia"] = abs(round((resta / df_final["Transferencia"]) * 100, 0))
    df_final["PorcentajeGarantia"] = 100 - df_final["PorcentajeTransferencia"]

    df_final["PorcentajeTransferencia"] = str_porcentaje(df_final["Transferencia"], df_final["PorcentajeTransferencia"])
    df_final["PorcentajeGarantia"] = str_porcentaje(df_final["Garantia"], df_final["PorcentajeGarantia"])

    fallas.save_consumo_df(df_final)


@execute_safely
def compute_fallas_garantias(df: pd.DataFrame, tipo_repuesto: str) -> None:
    df = df.loc[df["Tipo"] == "GARANTIA"]

    df = (df.groupby(GROUPBY_CAB_REP)
          .agg({"DiasColocado": "mean"})
          .rename(columns=CONSUMO_FALLAS_GARANTIAS_COLS_RENAME)
          .reset_index())
    
    df["PromedioTiempoFalla"] = df["PromedioTiempoFalla"].round(0)

    df.insert(3, "TipoRepuesto", tipo_repuesto)
    fallas.save_df(df)


def str_porcentaje(col_norm, col_porc) -> str:
    str_norm = col_norm.astype(int).astype(str)
    str_porc = col_porc.astype(int).astype(str)

    return str_norm + " (" + str_porc + "%)"


def group_tipo(df: pd.DataFrame, tipo: str, cols: list):
    df_final = df.loc[df["Tipo"] == tipo]

    return (df_final.groupby(GROUPBY_CAB_REP)
                    .agg({"Cantidad": "sum"})
                    .rename(columns=cols)
                    .reset_index())