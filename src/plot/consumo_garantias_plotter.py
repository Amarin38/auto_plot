import random

import plotly.graph_objects as go

from src.config.constants import COLORS
from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import db_to_df
from src.db_data.models.services_model.consumo_garantias_model import ConsumoGarantiasModel
from src.utils.streamlit_utils import update_layout


class ConsumoGarantiasPlotter:
    def __init__(self):
        self.df_data = db_to_df(ConsumoGarantiasModel)

    @execute_safely
    def create_plot(self):

        x_garantias = self.df_data["Cabecera"]
        y_garantias = self.df_data["Garantia"]

        x_transfer = self.df_data["Cabecera"]
        y_transfer = self.df_data["Transferencia"]

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
            textposition="outside",
            textfont=dict(
                size=11,
                color='white',
                family='Arial'
            ),

            marker=dict(color=COLORS[12])
        ))

        update_layout(fig,'Consumos Garantias y Transferencias', 'Cabecera', 'Consumo')
        return fig
