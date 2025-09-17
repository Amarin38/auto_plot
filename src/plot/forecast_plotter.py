import pandas as pd

import plotly.graph_objects as go

from src.config.constants import COLORS

from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import sql_to_df_by_type, read_date
from src.db_data.models.services_model.forecast_trend_model import ForecastTrendModel
from src.db_data.models.services_model.forecast_data_model import ForecastDataModel


class ForecastPlotter:
    @execute_safely
    def create_plot(self, tipo_rep: str):
        df_data = sql_to_df_by_type(ForecastDataModel, tipo_rep)
        df_trend = sql_to_df_by_type(ForecastTrendModel, tipo_rep)

        todos_repuestos = df_data["Repuesto"].unique()
        figuras = []
        
        for repuesto in todos_repuestos:
            x_data = df_data.loc[df_data["Repuesto"] == repuesto, "FechaCompleta"]
            y_data = df_data.loc[df_data["Repuesto"] == repuesto, "TotalMes"]
        
            x_tendencia = df_trend.loc[df_trend["Repuesto"] == repuesto, "FechaCompleta"]
            y_tendencia = df_trend.loc[df_trend["Repuesto"] == repuesto, "TendenciaEstacional"]

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
    def devolver_fecha(self) -> str:
        df_fecha = read_date(ForecastDataModel)
        return pd.to_datetime(df_fecha["FechaCompleta"].unique()).strftime("%d-%m-%Y")[0]
    
    
    @execute_safely
    def _devolver_titulo(self, rep: str) -> str:
        return f"Prevision de {rep} ({self.devolver_fecha()})"
