import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from config.constants import T_RED, RESET, T_YELLOW, T_ORANGE, T_BLUE
from utils.exception_utils import execute_safely
from viewmodels.prevision_data_vm import PrevisionDataVM
from viewmodels.prevision_vm import PrevisionVM


@execute_safely
def create_forecast(df: pd.DataFrame, tipo_repuesto: str):
    repuesto = df["Repuesto"].unique()

    for rep in repuesto:
        df_rep = df.loc[df["Repuesto"] == rep].copy()

        # Fechas
        df_rep["FechaCompleta"] = pd.to_datetime(df_rep["FechaCompleta"])
        df_rep = df_rep.groupby(df_rep["FechaCompleta"].dt.to_period("M")).agg({"Cantidad":"sum"})
        df_rep.index = pd.PeriodIndex(df_rep.index, freq='M').to_timestamp()
        df_rep = df_rep.asfreq("MS")
        df_rep = df_rep.replace(np.nan, 0)

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

            data: pd.DataFrame = series.to_frame("Consumo").reset_index() # type: ignore
            data.columns = ["FechaCompleta", "Consumo"]
            data["Consumo"] = data["Consumo"].round(0)
            data["Repuesto"] = rep
            data["TipoRepuesto"] = tipo_repuesto
            data["FechaCompleta"] = data["FechaCompleta"].dt.date
            PrevisionDataVM().save_df(data)

            prevision: pd.DataFrame = prevision.to_frame("Prevision").reset_index()# type: ignore
            prevision.columns = ["FechaCompleta", "Prevision"]
            prevision["Prevision"] = prevision["Prevision"].round(0)
            prevision["Prevision"] = prevision["Prevision"].clip(lower=0)
            prevision["Repuesto"] = rep
            prevision["TipoRepuesto"] = tipo_repuesto
            prevision["FechaCompleta"] = prevision["FechaCompleta"].dt.date
            PrevisionVM().save_df(prevision)

        except ValueError:
            print(f"""
         {T_RED}Error{RESET}: {T_YELLOW}No se puede calcular la previsión sin 2 años completos de datos.{RESET}
        {T_ORANGE} Faltan datos del repuesto:{RESET} {T_BLUE}{rep}{RESET}
        """)
            pass