import plotly.graph_objects as go

from src.config.constants import COLORS
from src.db_data.crud_services import ServiceRead
from src.db_data.models.services_model.consumo_garantias_model import ConsumoGarantiasModel
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import update_layout


class ConsumoGarantiasPlotter:
    def __init__(self, cabecera, tipo_repuesto):
        self.df_data = ServiceRead().by_rep_and_cabecera(ConsumoGarantiasModel, cabecera, tipo_repuesto)


    @execute_safely
    def create_plot(self):
        x_data = self.df_data["Repuesto"]
        y_garantias = self.df_data["Garantia"]
        y_transfer = self.df_data["Transferencia"]
        diferencia_gar = self.df_data["PorcentajeGarantia"]
        diferencia_transfer = self.df_data["PorcentajeTransferencia"]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x_data,
            y=y_garantias,
            name="Garantias",

            text=diferencia_gar,
            textposition="outside",
            textfont=dict(
                size=15,
                color='white',
                family='Arial'
            ),

            marker=dict(color=COLORS[1])
        ))

        fig.add_trace(go.Bar(
            x=x_data,
            y=y_transfer,
            name="Transferencia",

            text=diferencia_transfer,
            textposition="outside",
            textfont=dict(
                size=15,
                color='white',
                family='Arial'
            ),

            marker=dict(color=COLORS[12])
        ))
        update_layout(fig,'', 'Repuesto', 'Consumo', height=665)

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
