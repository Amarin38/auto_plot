import random

import plotly.graph_objects as go

from src.config.constants import COLORS
from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import db_to_df
from src.db_data.models.services_model.consumo_garantias_model import ConsumoGarantiasModel


class ConsumoGarantiasPlotter:
    @execute_safely
    def create_plot(self):
        df_data = db_to_df(ConsumoGarantiasModel)

        x_garantias = df_data["Cabecera"]
        y_garantias = df_data["Garantia"]

        x_transfer = df_data["Cabecera"]
        y_transfer = df_data["Transferencia"]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x_garantias,
            y=y_garantias,
            name="Garantias",

            text=y_garantias,
            textposition="auto",
            textfont=dict(
                size=11,
                color='white',
                family='Arial'
            ),

            marker=dict(color=COLORS[1])
        ))

        fig.add_trace(go.Bar(
            x=x_transfer,
            y=y_transfer,
            name="Transferencia",

            text=y_transfer,
            textposition="auto",
            textfont=dict(
                size=11,
                color='white',
                family='Arial'
            ),

            marker=dict(color=COLORS[12])
        ))

        fig.update_layout(
            title=f'Consumos Garantias y Transferencias',
            showlegend=True,

            xaxis=dict(
                title='Cabecera',
                showticklabels=True
            ),

            yaxis=dict(
                title='Consumo',
                showticklabels=True
            ),
        )

        return fig
