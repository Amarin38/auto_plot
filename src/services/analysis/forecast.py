import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from src.config.constants import COLORS, T_RED, RESET, T_YELLOW, T_ORANGE, T_BLUE
from src.db_data.crud_services import df_to_db
from src.utils.exception_utils import execute_safely

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

        # TODO: queda que haga el forecast por cada repuesto
        # Modelo HoltWinters para calcular el suavizado exponencial triple

        try:
            fit = ExponentialSmoothing(
                series,
                trend="add",
                seasonal="add",
                seasonal_periods=12
            ).fit()

            forecast: pd.Series = fit.forecast(12)

            data: pd.DataFrame = series.to_frame("Consumo").reset_index() # type: ignore
            data.columns = ["FechaCompleta", "Consumo"]
            data["Consumo"] = data["Consumo"].round(0)
            data["Repuesto"] = rep
            data["TipoRepuesto"] = tipo_repuesto
            data["FechaCompleta"] = data["FechaCompleta"].dt.date
            df_to_db("forecast_data", data)

            forecast: pd.DataFrame = forecast.to_frame("Prevision").reset_index()# type: ignore
            forecast.columns = ["FechaCompleta", "Prevision"]
            forecast["Prevision"] = forecast["Prevision"].round(0)
            forecast["Prevision"] = forecast["Prevision"].clip(lower=0)
            forecast["Repuesto"] = rep
            forecast["TipoRepuesto"] = tipo_repuesto
            forecast["FechaCompleta"] = forecast["FechaCompleta"].dt.date
            df_to_db("forecast", forecast)

        except ValueError:
            print(f"""
         {T_RED}Error{RESET}: {T_YELLOW}No se puede calcular la previsión sin 2 años completos de datos.{RESET}
        {T_ORANGE} Faltan datos del repuesto:{RESET} {T_BLUE}{rep}{RESET}
        """)
            pass

    # params = fit.model.params
    # print("Parámetros encontrados:")
    # for key, value in params.items():
    #     if isinstance(value, float):
    #         print(f"{key}: {value:.3f}")
    #     else:
    #         print(f"{key}: {value}")
    #
    # print("\nPronósticos:")
    # print(forecast)