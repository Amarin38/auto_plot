from typing import Tuple, Union, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from config.constants_colors import INDICE_MEDIA_COLOR, INDICE_COLORS
from config.enums import IndexTypeEnum

from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils

from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents, PlotComponents
from viewmodels.consumo.indice.vm import IndiceConsumoVM

class IndexPlotter:
    def __init__(self, index_type: IndexTypeEnum, tipo_rep: str) -> None:
        self.common = CommonUtils()
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.scatter = PlotComponents()

        self.tipo_rep = tipo_rep
        self.df = IndiceConsumoVM().get_df_tipo_repuesto_and_tipo_indice(tipo_rep, index_type)

    @execute_safely
    def create_plot(self) -> Union[Tuple[list, str], List[None]]:
        if not self.df.empty:
            titulo = f"Indice {self.tipo_rep} ({self.common.devolver_fecha(self.df, "UltimaFecha")})" \
                if self.tipo_rep else ""

            figuras = []

            todos_repuestos = self.df["Repuesto"].unique()
            grouped_repuesto = self.df.groupby("Repuesto")

            for repuesto, color in zip(todos_repuestos, INDICE_COLORS):
                df_repuesto = grouped_repuesto.get_group(repuesto)

                x_data = df_repuesto["Cabecera"]
                y_data = df_repuesto["ConsumoIndice"]
                median = [round(y_data.replace(0, np.nan).mean(), 1)] * len(x_data)
                avg = median[0]

                condicion_mayor = df_repuesto["ConsumoIndice"] > avg
                condicion_menor = df_repuesto["ConsumoIndice"] < avg
                condicion_igual = df_repuesto["ConsumoIndice"] == avg

                porcentaje_mayor = round((df_repuesto.loc[condicion_mayor, "ConsumoIndice"] * 100) / avg, 0) - 100
                porcentaje_menor = round((df_repuesto.loc[condicion_menor, "ConsumoIndice"] * 100) / avg, 0) - 100

                valores_mayores = y_data.loc[condicion_mayor]
                valores_menores = y_data.loc[condicion_menor]
                valores_iguales = y_data.loc[condicion_igual]

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=x_data,
                    y=y_data.to_numpy(),
                    name="Índice de consumo",
                    textposition="auto",
                    textfont=dict(
                        size=11,
                        color='white',
                        family='Arial'
                    ),
                    customdata=[color] * len(x_data),
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
                    name=f"Media {avg}",
                    line=dict(
                        color=INDICE_MEDIA_COLOR,
                        dash='dash'
                    ),
                    customdata=[INDICE_MEDIA_COLOR] * len(x_data),
                    hovertemplate = """
<b>
<span style='color:%{customdata}'>Media:</span>
</b>
%{y}
<extra></extra>
"""
                ))


                self.scatter.cross(fig, df_repuesto.loc[condicion_mayor, "Cabecera"], valores_mayores,
                                   "Superior a la media", "Encima de la media por", porcentaje_mayor)

                self.scatter.tick(fig, df_repuesto.loc[condicion_menor, "Cabecera"], valores_menores,
                                  "Inferior a la media", "Debajo de la media por", porcentaje_menor)

                self.scatter.mid_line(fig, df_repuesto.loc[condicion_igual, "Cabecera"], valores_iguales,
                                   "En la media", "En la media")


                self.default.update_layout(fig, repuesto, "Cabecera", "Indice de consumo")
                self.hover.hover_junto(fig)

                figuras.append(fig)
            return figuras, titulo
        return [None, None]