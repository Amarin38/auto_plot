import pandas as pd

import plotly.graph_objects as go

from typing import Literal

from src.config.constants import COLORS
from src.config.constants import MAIN_PATH

from src.utils.exception_utils import execute_safely
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.analysis.forecast.forecast_with_zero import ForecastWithZero
from src.utils.common_utils import CommonUtils

from src.db.crud import sql_to_df_by_type, read_date
from src.db.models.forecast_trend_model import ForecastTrend
from src.db.models.forecast_data_model import ForecastData


class ForecastPlotter:
    def __init__(self, directory: str, tipo_rep: str, with_zero: Literal["WITH ZERO", "WITHOUT ZERO"] = "WITH ZERO", months_to_forecast: int = 12) -> None:
        self.directory = directory
        self.tipo_rep = tipo_rep
        self.with_zero = with_zero
        self.months_to_forecast = months_to_forecast

        dir_exists = CommonUtils.check_file_exists(MAIN_PATH, directory)
        if dir_exists:
            self.prepare_data()
            
        self.df_tendencia = sql_to_df_by_type(ForecastTrend, self.tipo_rep)
        self.df_data = sql_to_df_by_type(ForecastData, self.tipo_rep)


    @execute_safely
    def create_plot(self):
        todos_repuestos = self.df_data["Repuesto"].unique()
        figuras = []

        
        for repuesto in todos_repuestos:
            x_data = self.df_data.loc[self.df_data["Repuesto"] == repuesto, "FechaCompleta"]
            y_data = self.df_data.loc[self.df_data["Repuesto"] == repuesto, "TotalMes"]
        
            x_tendencia = self.df_tendencia.loc[self.df_tendencia["Repuesto"] == repuesto, "FechaCompleta"]
            y_tendencia = self.df_tendencia.loc[self.df_tendencia["Repuesto"] == repuesto, "TendenciaEstacional"]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                name="Consumo",
                mode='lines+markers+text',

                text=y_data,
                textposition="top center",
                textfont=dict(
                    size=19,
                    color=COLORS[15]
                ),

                line=dict(color=COLORS[16], width=2),
                marker=dict(
                    color=COLORS[16],             
                    size=8,                  
                    symbol='circle',         
                ),
            ))


            fig.add_trace(go.Scatter(
                x=x_tendencia,
                y=y_tendencia,
                name="Tendencia",
                mode='lines+markers+text',

                text=y_tendencia,
                textposition="top center",
                textfont=dict(
                    size=19,
                    color=COLORS[1]
                ),
 
                line=dict(color=COLORS[3], width=2, dash='dash'),
                marker=dict(
                    color=COLORS[3],             
                    size=8,                  
                    symbol='square',         
                ),
            ))


            fig.update_layout(
                title=f"{repuesto}",
                showlegend=True,

                xaxis=dict(
                    title='Fecha',
                    showticklabels=True
                ),

                yaxis=dict(
                    title='Consumo',
                    showticklabels=True
                ),
            )

            figuras.append(fig)
        return figuras
    

    @execute_safely
    def prepare_data(self) -> None:
        """
        ### Prepara los datos para graficar.
        """
        df = InventoryDataCleaner().run_all(self.directory)
        ForecastWithZero(df, self.directory, self.tipo_rep, self.months_to_forecast).create_forecast()


    @execute_safely
    def devolver_fecha(self) -> str:
        df_fecha = read_date(ForecastData)
        return pd.to_datetime(df_fecha["FechaCompleta"].unique()).strftime("%d-%m-%Y")[0]
    
    
    @execute_safely
    def devolver_titulo(self, rep) -> str:
        return f"Indice {rep} ({self.devolver_fecha()})"
