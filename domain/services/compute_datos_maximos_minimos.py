import datetime
from typing import Optional

import numpy as np
import pandas as pd

from utils.exception_utils import execute_safely

@execute_safely
def calculate_maxmin(df: Optional[pd.DataFrame] = None, mult_por_min: float = 1, mult_por_max: float = 2) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()

    keys = ["FamiliaStock", "ArticuloStock", "DescripcionStock", "CabeceraStock"]
    df["Stock"] = pd.to_numeric(df["Stock"], errors="coerce")
    df_copy = df.copy()[keys + ["FechaStock", "Stock"]]

    df_grouped = df_copy.groupby(keys).agg({"Stock":"mean"}).reset_index()
    df_grouped = df_grouped.rename(columns={
        "FamiliaStock": "Familia",
        "ArticuloStock": "Articulo",
        "DescripcionStock": "Descripcion",
        "CabeceraStock": "Cabecera",
        "FechaStock": "Fecha",
    })

    df_grouped["Fecha"] = pd.to_datetime(datetime.date.today(), errors="coerce", format="%Y-%m-%d")
    div_seis_meses = round(df_grouped["Stock"] / 1, 1)
    df_grouped["Minimo"] = np.ceil(div_seis_meses * mult_por_min)
    df_grouped["Maximo"] = np.ceil(div_seis_meses * mult_por_max)
    df_grouped["Cabecera"] = df_grouped["Cabecera"].fillna("").astype(str)
    df_grouped["Descripcion"] = df_grouped["Descripcion"].fillna("").astype(str)
    df_grouped = df_grouped.drop("Stock", axis=1)
    #df_grouped.

    return df_grouped
