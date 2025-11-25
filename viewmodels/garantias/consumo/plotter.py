from typing import Union

import pandas as pd
import plotly.graph_objects as go

from config.constants import COLORS, CONSUMO_GARANTIAS_COLORS
from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout, hover_junto
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


            color_garantias = CONSUMO_GARANTIAS_COLORS[0]
            color_transferencias = CONSUMO_GARANTIAS_COLORS[1]

            custom_garantias = list(zip(pd.Series("Garantias", index=x_data),
                                        pd.Series(color_garantias, index=x_data)))

            custom_transferencias = list(zip(pd.Series("Transferencias", index=x_data),
                                             pd.Series(color_transferencias, index=x_data)))

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x_data,
                y=y_garantias,
                name="Garantias",

                text=diferencia_gar,
                textposition="none",
                textfont=dict(
                    size=15,
                    color='white',
                    family='Arial'
                ),

                marker=dict(color=color_garantias),
                customdata=custom_garantias,
                hovertemplate = """
<b>
<span style='color:%{customdata[1]}'>%{customdata[0]}:</span>
<span style='color:white'>%{text} </span>
</b>
<extra></extra>
"""
            ))

            fig.add_trace(go.Bar(
                x=x_data,
                y=y_transfer,
                name="Transferencia",

                text=diferencia_transfer,
                textposition="none",
                textfont=dict(
                    size=15,
                    color='white',
                    family='Arial'
                ),

                marker=dict(color=color_transferencias),
                customdata=custom_transferencias,
                hovertemplate = """
<b>
<span style='color:%{customdata[1]}'>%{customdata[0]}:</span>
<span style='color:white'>%{text} </span>
</b>
<extra></extra>
""",
            ))


            update_layout(fig,'Consumo garantias frente a transferencias', 'Repuesto', 'Consumo', height=665)

            fig.update_layout(
                # legend=dict(
                #     orientation='h',
                #     yanchor='top',
                #     y=1.15,
                #     xanchor='left',
                #     x=-0.01,
                #     font=dict(size=13),
                #     bgcolor=COLORS[4],
                #     bordercolor=COLORS[5],
                # ),
                showlegend=False,
            )

            hover_junto(fig)
            return fig
        return None