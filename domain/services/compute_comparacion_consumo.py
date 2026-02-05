import pandas as pd

from config.enums import ConsumoComparacionRepuestoEnum, PeriodoComparacionEnum
from viewmodels.common.json_config_vm import JSONConfigVM
from viewmodels.consumo.comparacion.vm import ConsumoComparacionVM


def compute_comparacion_consumo(df: pd.DataFrame, tipo_rep: ConsumoComparacionRepuestoEnum) -> None:
    if df.empty:
        return None

    df: pd.DataFrame = df.copy()[["Familia", "Articulo", "Repuesto", "movnom",  # type: ignore
                                  "Cantidad", "Precio", "FechaCompleta"]]
    df = df.rename(columns={"movnom": "Cabecera", "Cantidad":"Consumo", "Precio": "Gasto"})
    df.insert(3, "TipoRepuesto", tipo_rep)

    df["Cabecera"] = df["Cabecera"].str[-2:].str.strip()
    df["Cabecera"] = df["Cabecera"].map(JSONConfigVM().get_df_by_id("transferencias"))
    df["Cabecera"] = df["Cabecera"].astype(str)

    fecha_min = pd.to_datetime(df["FechaCompleta"], errors="coerce").min()
    fecha_max = pd.to_datetime(df["FechaCompleta"], errors="coerce").max()

    periodo = None

    if fecha_min.year == 2020 and (fecha_max.year == 2020, fecha_max.year == 2021):
        periodo = PeriodoComparacionEnum.DESDE_2020_A_2021
    elif fecha_min.year == 2021 and (fecha_max.year == 2021 or fecha_max.year == 2022):
        periodo = PeriodoComparacionEnum.DESDE_2021_A_2022
    elif fecha_min.year == 2022 and (fecha_max.year == 2022 or fecha_max.year == 2023):
        periodo = PeriodoComparacionEnum.DESDE_2022_A_2023
    elif fecha_min.year == 2023 and (fecha_max.year == 2023 or fecha_max.year == 2024):
        periodo = PeriodoComparacionEnum.DESDE_2023_A_2024
    elif fecha_min.year == 2024 and (fecha_max.year == 2024 or fecha_max.year == 2025):
        periodo = PeriodoComparacionEnum.DESDE_2024_A_2025
    elif fecha_min.year == 2025 and (fecha_max.year == 2025 or fecha_max.year == 2026):
        periodo = PeriodoComparacionEnum.DESDE_2025_A_2026

    df["PeriodoID"] = periodo

    df["Familia"]       = df["Familia"].astype("int16")
    df["Articulo"]      = df["Articulo"].astype("int32")
    df["Repuesto"]      = df["Repuesto"].astype("category")
    df["TipoRepuesto"]  = df["TipoRepuesto"].astype("category")
    df["Consumo"]       = df["Consumo"].astype(str).str.replace(",",".").astype("float64").round(1)
    df["Gasto"]         = df["Gasto"].astype(str).str.replace(",",".").astype("float64").round(1)
    df["PeriodoID"]     = df["PeriodoID"].astype("category")
    df["FechaCompleta"] = df["FechaCompleta"].astype("datetime64[ns]")

    ConsumoComparacionVM().save_df(df)
    return None
