import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from config.constants_common import FILE_STRFTIME_YMD
from config.enums import RepuestoEnum
from config.enums_colors import TextModsEnum, ForegroundColorsEnum
from viewmodels.consumo.prevision.data_vm import PrevisionDataVM
from viewmodels.consumo.prevision.vm import PrevisionVM


def create_forecast(df: pd.DataFrame, tipo_repuesto: RepuestoEnum):
    repuesto = df["Repuesto"].unique()

    for rep in repuesto:
        df_rep = df.loc[df["Repuesto"] == rep].copy()

        # Fechas
        df_rep["FechaCompleta"] = pd.to_datetime(df_rep["FechaCompleta"])
        df_rep["Cantidad"]      = pd.to_numeric(df_rep["Cantidad"], errors="coerce")
        df_rep                  = df_rep.groupby(df_rep["FechaCompleta"].dt.to_period("M")).agg({"Cantidad":"sum"})
        df_rep.index            = pd.PeriodIndex(df_rep.index, freq='M').to_timestamp()
        df_rep                  = df_rep.asfreq("MS")
        df_rep                  = df_rep.replace(np.nan, 0)

        series: pd.Series = pd.Series(df_rep["Cantidad"].values, index=df_rep.index)

        # Modelo HoltWinters para calcular el suavizado exponencial triple
        try:
            fit = ExponentialSmoothing(
                series,
                trend="add",
                seasonal="add",
                seasonal_periods=12
            ).fit()

            prevision: pd.Series = fit.forecast(12)

            data: pd.DataFrame      = series.to_frame("Consumo").reset_index()
            data.columns            = ["FechaCompleta", "Consumo"]
            data["Consumo"]         = data["Consumo"].round(0)
            data["Consumo"]         = data["Consumo"].astype("float16")
            data["Repuesto"]        = rep
            data["TipoRepuesto"]    = tipo_repuesto
            data["FechaCompleta"]   = data["FechaCompleta"].dt.date

            PrevisionDataVM().save_df(data)

            prevision: pd.DataFrame         = prevision.to_frame("ConsumoPrevision").reset_index()
            prevision.columns               = ["FechaCompleta", "ConsumoPrevision"]
            prevision["ConsumoPrevision"]   = prevision["ConsumoPrevision"].round(0)
            prevision["ConsumoPrevision"]   = prevision["ConsumoPrevision"].clip(lower=0)
            prevision["ConsumoPrevision"]   = prevision["ConsumoPrevision"].astype("float64")
            prevision["Repuesto"]           = rep
            prevision["TipoRepuesto"]       = tipo_repuesto
            prevision["FechaCompleta"]      = prevision["FechaCompleta"].dt.date

            PrevisionVM().save_df(prevision)

        except ValueError as e:
            print(f"""
         {ForegroundColorsEnum.T_RED}Error{TextModsEnum.RESET}: {ForegroundColorsEnum.T_YELLOW}No se puede calcular la previsión sin 2 años completos de datos.{TextModsEnum.RESET}
        {ForegroundColorsEnum.T_ORANGE} Faltan datos del repuesto:{TextModsEnum.RESET} {ForegroundColorsEnum.T_BLUE}{rep}{TextModsEnum.RESET}
        {e.with_traceback(e.__traceback__)}
        """)
            pass


def create_forecast_gs(df: pd.DataFrame, df_stock: pd.DataFrame, tipo_repuesto: str):
    df = df.replace("", pd.NA).dropna(subset=["Mes", "Articulo"])
    nombre_articulos = df["Articulo"].unique()

    lista_previsiones = []

    for articulo in nombre_articulos:
        df_art = df.loc[df["Articulo"] == articulo].copy()

        df_art["Mes"] = pd.to_datetime(df_art["Mes"], dayfirst=True)
        df_art["ConsumoMensual"] = pd.to_numeric(df_art["ConsumoMensual"], errors="coerce")

        df_art = df_art.set_index("Mes")
        df_art = df_art.resample("MS").sum()
        df_art["ConsumoMensual"] = df_art["ConsumoMensual"].fillna(0).astype("float64")

        df_stock_art = df_stock.loc[df_stock["RepuestoStock"] == articulo].copy()

        try:
            data: pd.Series = df_art["ConsumoMensual"]

            # Modelo HoltWinters
            fit = ExponentialSmoothing(
                data,
                trend="add",
                damped_trend=True,
                seasonal="add",
                seasonal_periods=12,
                initialization_method="estimated"
            ).fit(optimized=True)

            prevision: pd.Series = fit.forecast(12)
            ultima_fecha = data.index[-1]
            prevision.index = pd.date_range(start=ultima_fecha + pd.DateOffset(months=1), periods=12, freq='MS')

            df_prev = prevision.to_frame(name="Prevision").reset_index()
            df_prev.columns = ["FechaPrevision", "Prevision"]
            df_prev["Prevision"] = df_prev["Prevision"].round(0).clip(lower=0).astype("float64")
            df_prev["RestoStock"] = df_stock_art["StockActual"].iloc[0] - df_prev["Prevision"].cumsum()
            df_prev["RepuestoPrevision"] = articulo
            df_prev["TipoRepuestoPrevision"] = tipo_repuesto
            df_prev["FechaPrevision"] = df_prev["FechaPrevision"].dt.strftime(FILE_STRFTIME_YMD)

            lista_previsiones.append(df_prev)
        except ValueError as e:
            print(f"Omitiendo repuesto {articulo} por falta de datos. Detalle: {e}")
            continue

    if lista_previsiones:
        final_prevision = pd.concat(lista_previsiones, ignore_index=True)
        return final_prevision
    else:
        return None