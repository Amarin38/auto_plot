import random
from typing import Tuple, Union, List

import numpy as np
import plotly.graph_objects as go

from config.constants import COLORS
from config.enums import IndexTypeEnum

from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout, devolver_fecha, top_right_legend, hover_unified
from viewmodels.consumo.indice.vm import IndiceConsumoVM


class IndexPlotter:
    def __init__(self, index_type: IndexTypeEnum, tipo_rep: str) -> None:
        self.tipo_rep = tipo_rep
        self.df = IndiceConsumoVM().get_df_tipo_repuesto_and_tipo_indice(tipo_rep, index_type)

    @execute_safely
    def create_plot(self) -> Union[Tuple[list, str], List[None]]:
        if not self.df.empty:
            if self.tipo_rep:
                titulo = f"Indice {self.tipo_rep} ({devolver_fecha(self.df, "UltimaFecha")})"
            else:
                titulo = ""

            todos_repuestos = self.df["Repuesto"].unique()
            figuras = []

            for repuesto in todos_repuestos:
                df_repuesto = self.df.loc[self.df["Repuesto"] == repuesto]

                x_data = df_repuesto["Cabecera"]
                y_data = df_repuesto["ConsumoIndice"]
                median = [round(y_data.replace(0, np.nan).mean(), 1)] * len(x_data)

                condicion_mayor = df_repuesto["ConsumoIndice"] > median[0]
                porcentaje = round((df_repuesto.loc[condicion_mayor, "ConsumoIndice"] * 100) / median[0], 0) -100

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=x_data,
                    y=y_data,
                    name="Índice de consumo",

                    text=y_data,
                    textposition="auto",
                    textfont=dict(
                        size=11,
                        color='white',
                        family='Arial'
                    ),

                    marker=dict(color=COLORS[random.randint(0,19)]),
                    hovertemplate = """
<b>
<span style='color:white'>Índice:</span>
</b>
%{y}
<extra></extra>
"""
                ))


                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=median,
                    mode="lines",
                    name=f"Media {median[0]}",
                    line=dict(color='#FF5733', dash='dash'),
                    hovertemplate = """
<b>
<span style='color:#FF5733'>Media:</span>
</b>
%{y}
<extra></extra>
"""
                ))

                fig.add_trace(go.Scatter(
                        x=df_repuesto.loc[condicion_mayor, "Cabecera"],
                        y=y_data.loc[condicion_mayor]+5,
                        mode="markers",
                        name="Supera la media",
                        marker=dict(
                            size=10,
                            color="#C70039",
                            symbol="x",
                            line=dict(width=0.5),
                        ),
                        legendgroup="B",
                        customdata=porcentaje,
                        hovertemplate="""
<b>
<span style='color:#C70039'>Encima de la media por:</span>
</b>
%{customdata}%
<extra></extra>
"""
                    )
                )

                update_layout(fig, repuesto, "Cabecera", "Indice de consumo")
                # top_right_legend(fig)
                hover_unified(fig)

                figuras.append(fig)
            return figuras, titulo
        return [None, None]