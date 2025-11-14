from typing import Union

import plotly.graph_objects as go

from config.constants import COLORS
from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout
from viewmodels.garantias.consumo.vm import ConsumoGarantiasVM


class ConsumoGarantiasPlotter:
    def __init__(self, tipo_repuesto, cabecera):
        self.df_data = ConsumoGarantiasVM().get_df_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)


    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df_data.empty:
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
        return None