import pandas as pd

import plotly.graph_objects as go

from src.config.constants import COLORS, FILE_STRFTIME_YMD

from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import ServiceRead
from src.db_data.models.services_model.forecast_model import ForecastModel
from src.db_data.models.services_model.forecast_data_model import ForecastDataModel
from src.utils.streamlit_utils import update_layout, devolver_fecha, range_slider, top_right_legend


class ForecastPlotter:
    def __init__(self, tipo_rep: str):
        db = ServiceRead()
        self.tipo_rep = tipo_rep
        self.df_data = db.by_tipo_repuesto(ForecastDataModel, self.tipo_rep)
        self.df_forecast = db.by_tipo_repuesto(ForecastModel, self.tipo_rep)


    @execute_safely
    def create_plot(self):
        figuras = []
        todos_repuestos = self.df_data['Repuesto'].unique()

        self.df_data['FechaCompleta'] = pd.to_datetime(self.df_data['FechaCompleta'], format=FILE_STRFTIME_YMD)
        self.df_forecast['FechaCompleta'] = pd.to_datetime(self.df_forecast['FechaCompleta'], format=FILE_STRFTIME_YMD)
        
        if self.tipo_rep:
            titulo = f'Prevision de {self.tipo_rep} ({devolver_fecha(self.df_data, "FechaCompleta")})'
        else:
            titulo = ""
        

        for repuesto in todos_repuestos:
            x_data = self.df_data.loc[self.df_data['Repuesto'] == repuesto, 'FechaCompleta']
            y_data = self.df_data.loc[self.df_data['Repuesto'] == repuesto, 'Consumo']

            x_forecast = self.df_forecast.loc[self.df_forecast['Repuesto'] == repuesto, 'FechaCompleta']
            y_forecast = self.df_forecast.loc[self.df_forecast['Repuesto'] == repuesto, 'Prevision']

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
                name=f'Prevision ({y_forecast.sum()})',
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

            update_layout(fig, repuesto, "Fecha", "Consumo")
            range_slider(fig)
            top_right_legend(fig)

            figuras.append(fig)
        return figuras, titulo

