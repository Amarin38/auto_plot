import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from src.db_data.crud_services import df_to_db
from src.utils.exception_utils import execute_safely

@execute_safely
def create_forecast(df: pd.DataFrame, tipo_repuesto: str):
    repuesto = df["Repuesto"].unique()[0]

    df["FechaCompleta"] = pd.to_datetime(df["FechaCompleta"])
    df = df.groupby(df["FechaCompleta"].dt.to_period("M")).agg({"Cantidad":"sum"})
    df.index = pd.PeriodIndex(df.index, freq='M').to_timestamp()
    df = df.asfreq("MS")
    df = df.replace(np.nan, 0)

    series: pd.Series = pd.Series(df["Cantidad"].values, index=df.index)
    print(series)
    # Modelo HoltWinters para calcular el suavizado exponencial triple
    fit = ExponentialSmoothing(
        series,
        trend="add",
        seasonal="add",
        seasonal_periods=12
    ).fit()

    forecast: pd.Series = fit.forecast(12)
    params = fit.model.params

    print("Parámetros encontrados:")
    for key, value in params.items():
        if isinstance(value, float):
            print(f"{key}: {value:.3f}")
        else:
            print(f"{key}: {value}")

    print("\nPronósticos:")
    print(forecast)

    data: pd.DataFrame = series.to_frame("Consumo").reset_index() # type: ignore
    data.columns = ["FechaCompleta", "Consumo"]
    data["Consumo"] = data["Consumo"].round(0)
    data["Repuesto"] = repuesto
    data["TipoRepuesto"] = tipo_repuesto
    df_to_db("forecast_data", data)

    forecast: pd.DataFrame = forecast.to_frame("Prevision").reset_index()# type: ignore
    forecast.columns = ["FechaCompleta", "Prevision"]
    forecast["Prevision"] = forecast["Prevision"].round(0)
    forecast["Repuesto"] = repuesto
    forecast["TipoRepuesto"] = tipo_repuesto
    df_to_db("forecast", forecast)


# @execute_safely
# def create_forecast(df: pd.DataFrame, meses: int, tipo_repuesto: str, grado: int) -> pd.DataFrame:
#     df_list: List[pd.DataFrame] = []
#     repuestos = df["Repuesto"].unique()

#     for rep in repuestos:
#         df_rep: pd.DataFrame = df[df["Repuesto"] == rep] # separo por repuesto

#         # Ventas históricas y meses
#         ventas = df_rep["Cantidad"].to_numpy()
#         ventas = np.nan_to_num(ventas)


#         ultimo_mes = df_rep["FechaCompleta"].max().to_timestamp()
#         meses_actuales = df_rep["FechaCompleta"].dt.month.to_numpy()

#         meses_futuros = pd.date_range(
#             start=ultimo_mes + pd.DateOffset(months=1),  # arranca el mes siguiente
#             periods=meses,
#             freq="MS"  # "MS" = Month Start
#         )

#         meses_futuros_numpy = meses_futuros.month.to_numpy()


#         # Tendencia polinómica
#         if len(ventas) == 1:
#             tendencia_futura = np.full(meses, ventas[0])
#             estacionalidad_futura = np.ones(meses)
#         else:
#             if len(ventas) > grado:
#                 coeficientes = np.polyfit(meses_actuales, ventas, grado)
#                 tendencia_futura = np.polyval(coeficientes, meses_futuros_numpy)
#             else:
#                 # No se puede ajustar polinomio, usar promedio simple
#                 tendencia_futura = np.full(meses, ventas.mean())


#         # Estacionalidad
#         estacionalidad_mensual = df_rep.groupby("FechaCompleta")["Cantidad"].mean().reindex(np.arange(1,13), fill_value=ventas.mean()).to_numpy()
#         estacionalidad_futura = estacionalidad_mensual[:meses]


#         # Calculo la prevision
#         prevision = tendencia_futura + estacionalidad_futura
#         prevision = np.maximum(prevision, 0)

#         total_prevision = prevision.sum()

#         df_forecast = pd.DataFrame({
#                                     "Repuesto": rep,
#                                     "TipoRepuesto": tipo_repuesto,
#                                     "Prevision": np.round(prevision, 0),
#                                     "TotalPrevision": np.round(total_prevision, 0)
#                                     })
#         df_forecast["FechaCompleta"] = meses_futuros

#         print(df_forecast)
#         df_list.append(df_forecast)
#     df_final = pd.concat(df_list, ignore_index=True)
#     return df_final


