from typing import Tuple, Union, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from config.constants import INDICE_MEDIA_COLOR, INDICE_COLORS
from config.enums import IndexTypeEnum

from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils

from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents
from viewmodels.consumo.indice.vm import IndiceConsumoVM

class IndexPlotter:
    def __init__(self, index_type: IndexTypeEnum, tipo_rep: str) -> None:
        self.common = CommonUtils()
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()

        self.tipo_rep = tipo_rep
        self.df = IndiceConsumoVM().get_df_tipo_repuesto_and_tipo_indice(tipo_rep, index_type)

    @execute_safely
    def create_plot(self) -> Union[Tuple[list, str], List[None]]:
        if not self.df.empty:
            if self.tipo_rep:
                titulo = f"Indice {self.tipo_rep} ({self.common.devolver_fecha(self.df, "UltimaFecha")})"
            else:
                titulo = ""

            todos_repuestos = self.df["Repuesto"].unique()
            figuras = []

            iter_colors = iter(INDICE_COLORS)

            for repuesto in todos_repuestos:
                color = next(iter_colors, None)

                df_repuesto = self.df.loc[self.df["Repuesto"] == repuesto]

                x_data = df_repuesto["Cabecera"]
                y_data = df_repuesto["ConsumoIndice"]
                median = [round(y_data.replace(0, np.nan).mean(), 1)] * len(x_data)

                condicion_mayor = df_repuesto["ConsumoIndice"] > median[0]
                condicion_menor = df_repuesto["ConsumoIndice"] < median[0]
                condicion_igual = df_repuesto["ConsumoIndice"] == median[0]

                porcentaje_mayor = round((df_repuesto.loc[condicion_mayor, "ConsumoIndice"] * 100) / median[0], 0) - 100
                porcentaje_menor = round((df_repuesto.loc[condicion_menor, "ConsumoIndice"] * 100) / median[0], 0) - 100

                valores_mayores = y_data.loc[condicion_mayor]
                valores_menores = y_data.loc[condicion_menor]
                valores_iguales = y_data.loc[condicion_igual]

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=x_data,
                    y=y_data,
                    name="Índice de consumo",
                    textposition="auto",
                    textfont=dict(
                        size=11,
                        color='white',
                        family='Arial'
                    ),
                    customdata=pd.Series(color, x_data),
                    marker=dict(color=color),
                    hovertemplate = """
<b>
<span style='color:%{customdata}'>Índice:</span>
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
                    line=dict(
                        color=INDICE_MEDIA_COLOR,
                        dash='dash'
                    ),
                    customdata=pd.Series(INDICE_MEDIA_COLOR, x_data),
                    hovertemplate = """
<b>
<span style='color:%{customdata}'>Media:</span>
</b>
%{y}
<extra></extra>
"""
                ))


                fig.add_trace(go.Scatter(
                        x=df_repuesto.loc[condicion_mayor, "Cabecera"],
                        y=[v + 1 for v in valores_mayores],
                        mode="markers",
                        name="Superior a la media",
                        marker=dict(
                            size=10,
                            color="#C70039",
                            symbol="x",
                            line=dict(width=0.5),
                        ),
                        legendgroup="B",
                        customdata=porcentaje_mayor,
                        hovertemplate="""
<b>
<span style='color:#C70039'>Encima de la media por:</span>
</b>
%{customdata}%
<extra></extra>
"""
                    )
                )

                fig.add_trace(go.Scatter(
                    x=df_repuesto.loc[condicion_menor, "Cabecera"],
                    y=[v + 1 for v in valores_menores],
                    mode="markers+text",
                    name="Inferior a la media",
                    marker=dict(
                        size=11,
                        color="#3A7D44",
                        symbol="circle",
                        line=dict(width=0.5),
                    ),
                    text=["✔"] * 15,
                    legendgroup="B",
                    customdata=porcentaje_menor,
                    hovertemplate="""
<b>
<span style='color:#3A7D44'>Debajo de la media por:</span>
</b>
%{customdata}%
<extra></extra>
"""
                ))

                fig.add_trace(go.Scatter(
                    x=df_repuesto.loc[condicion_igual, "Cabecera"],
                    y=[v + 1 for v in valores_iguales],
                    mode="markers",
                    name="En la media",
                    marker=dict(
                        size=11,
                        color="#F2C14E",
                        symbol="line-ew-open",
                        line=dict(width=2),
                    ),
                    legendgroup="B",
                    hovertemplate="""
<b>
<span style='color:#F2C14E'>En la media</span>
</b>
<extra></extra>
"""
                ))

                self.default.update_layout(fig, repuesto, "Cabecera", "Indice de consumo")
                self.hover.hover_junto(fig)

                figuras.append(fig)
            return figuras, titulo
        return [None, None]