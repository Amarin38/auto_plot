import pandas as pd

import plotly.graph_objects as go

from src.config.constants import COLORS

from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import db_to_df_by_repuesto, read_date
from src.db_data.models.services_model.forecast_model import ForecastModel
from src.db_data.models.services_model.forecast_data_model import ForecastDataModel


class ForecastPlotter:
    @execute_safely
    def create_plot(self, tipo_rep: str):
        df_data = db_to_df_by_repuesto(ForecastDataModel, tipo_rep)
        df_forecast = db_to_df_by_repuesto(ForecastModel, tipo_rep)

        todos_repuestos = df_data['Repuesto'].unique()
        figuras = []
        
        for repuesto in todos_repuestos:
            x_data = df_data.loc[df_data['Repuesto'] == repuesto, 'FechaCompleta']
            y_data = df_data.loc[df_data['Repuesto'] == repuesto, 'Cantidad']
        
            x_forecast = df_forecast.loc[df_forecast['Repuesto'] == repuesto, 'FechaCompleta']
            y_forecast = df_forecast.loc[df_forecast['Repuesto'] == repuesto, 'Prevision']

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                name='Consumo',
                mode='lines+markers+text',

                text=y_data,
                textposition='top center',
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
                x=x_forecast,
                y=y_forecast,
                name='Prevision',
                mode='lines+markers+text',

                text=y_forecast,
                textposition='top center',
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
                title=f'{repuesto}',
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
        return figuras, df_data, df_forecast
    

    @execute_safely
    def devolver_fecha(self) -> str:
        df_fecha = read_date(ForecastDataModel)
        return pd.to_datetime(df_fecha['FechaCompleta'].unique()).strftime('%d-%m-%Y')[0]
    
    
    @execute_safely
    def devolver_titulo(self, rep: str) -> str:
        return f'Prevision de {rep} ({self.devolver_fecha()})'
