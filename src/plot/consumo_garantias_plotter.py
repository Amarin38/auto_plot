import plotly.graph_objects as go

from src.config.constants import COLORS
from src.db_data.crud_services import db_to_df
from src.db_data.models.services_model.consumo_garantias_model import ConsumoGarantiasModel
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import update_layout


class ConsumoGarantiasPlotter:
    def     __init__(self):
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
            textposition="outside",
            textfont=dict(
                size=12,
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
                size=14,
                color='white',
                family='Arial'
            ),

            marker=dict(color=COLORS[12])
        ))
        update_layout(fig,'', 'Cabecera', 'Consumo', height=665)

        fig.update_layout(
            legend=dict(
                orientation='h',
                yanchor='top',
                y=1.15,
                xanchor='left',
                x=-0.01,
                font=dict(size=13),
                bgcolor=COLORS[4],
                bordercolor=COLORS[5],
            ),
        )

        return fig
