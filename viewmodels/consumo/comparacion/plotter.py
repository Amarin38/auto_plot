from typing import Any, Tuple, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pandas import Series
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots
from itertools import product

from config.enums import PeriodoComparacionEnum, ConsumoComparacionRepuestoEnum, CabecerasEnum
from config.enums_colors import DuracionRepuestosColorsEnum, IndiceColorsEnum
from config.constants_common import FILE_STRFTIME_YMD
from utils.exception_utils import execute_safely
from viewmodels.consumo.comparacion.vm import ConsumoComparacionVM
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents


class ConsumoComparacionPlotter:
    def __init__(self, cabecera: CabecerasEnum, tipo_repuesto: List[ConsumoComparacionRepuestoEnum], periodo: List[PeriodoComparacionEnum]):
        self.cabecera = cabecera
        self.tipo_repuesto = tipo_repuesto
        self.periodo = periodo

        self.hover              = HoverComponents()
        self.default            = DefaultUpdateLayoutComponents()
        self.df                 = ConsumoComparacionVM().get_df_cabecera_and_tipo_rep_and_periodo(self.cabecera,
                                                                                                  self.tipo_repuesto,
                                                                                                  self.periodo)

    @execute_safely
    def create_plot(self) -> Any | None:
        if not self.df.empty:
            titulo = f"{self.cabecera} comparacion {self.tipo_repuesto} ({self.periodo})"

            agrupado = self.df.groupby(["Cabecera", "TipoRepuesto", "PeriodoID"]).agg({"Consumo":"sum"}).reset_index()
            print(agrupado)

            fig = go.Figure()

            periodos_unicos = agrupado["PeriodoID"].unique()

            for periodo, color in zip(periodos_unicos, IndiceColorsEnum.as_list()):
                datos_periodo = agrupado[agrupado["PeriodoID"] == periodo]

                x = datos_periodo["TipoRepuesto"]
                y = datos_periodo["Consumo"]

                cd = np.stack((
                    y,
                    [str(periodo)] * len(x)
                ), axis=-1)

                fig.add_trace(go.Bar(
                     x=x,
                     y=y.to_numpy(),
                     name=str(periodo),
                     textposition="auto",
                     textfont=dict(
                         size=11,
                         color='white',
                         family='Arial'
                     ),
                     customdata=cd,
                     marker=dict(color=color),
                     hovertemplate="""
<b>
<span style='color:%{marker.color}'>%{customdata[1]}:</span>
</b>
%{customdata[0]:.0f} (%{y:.0f}%)
<extra></extra>
"""
                                ))

            fig.update_layout(
                title=f"Comparativa: {self.cabecera}",
                xaxis_title="Tipo de Repuesto",
                legend_title="Periodo",
                barmode='group',
                barnorm='percent',  # Esto estira ambos periodos al mismo techo (100%)
                yaxis_title="Proporción del Consumo (%)",
                height=500
            )
            self.hover.hover_junto(fig)

            return agrupado, fig

    #         for repuesto, color in zip(todos_repuestos, IndiceColorsEnum.as_list()):
    #
    #             x = df_repuesto["TipoRepuesto"]
    #             y = df_repuesto["Consumo"]
    #             # median = [round(y_data.replace(0, np.nan).mean(), 1)] * len(x_data)
    #             # avg = median[0]
    #
    #             fig.add_trace(go.Bar(
    #                 x=x,
    #                 y=y.to_numpy(),
    #                 name="Índice de consumo",
    #                 textposition="auto",
    #                 textfont=dict(
    #                     size=11,
    #                     color='white',
    #                     family='Arial'
    #                 ),
    #                 customdata=[color] * len(x),
    #                 marker=dict(color=color),
    #                 hovertemplate="""
    # <b>
    # <span style='color:%{customdata}'>Índice:</span>
    # </b>
    # %{y}
    # <extra></extra>
    # """
    #             ))
    #
    #         # self.default.update_layout(fig, repuesto, "Cabecera", "Indice de consumo")
    #
    #         return fig, titulo
    #     return None, None
    #             fig.add_trace(go.Scatter(
    #                 x=x_data,
    #                 y=median,
    #                 mode="lines",
    #                 name=f"Media {avg}",
    #                 line=dict(
    #                     color=IndiceColorsEnum.NARANJA_OSCURO,
    #                     dash='dash'
    #                 ),
    #                 customdata=[IndiceColorsEnum.NARANJA_OSCURO] * len(x_data),
    #                 hovertemplate="""
    # <b>
    # <span style='color:%{customdata}'>Media:</span>
    # </b>
    # %{y}
    # <extra></extra>
    # """
    #             ))

                # self.scatter.cross(fig, df_repuesto.loc[condicion_mayor, "Cabecera"], valores_mayores,
                #                    "Superior a la media", "Encima de la media por", porcentaje_mayor)
                #
                # self.scatter.tick(fig, df_repuesto.loc[condicion_menor, "Cabecera"], valores_menores,
                #                   "Inferior a la media", "Debajo de la media por", porcentaje_menor)
                #
                # self.scatter.mid_line(fig, df_repuesto.loc[condicion_igual, "Cabecera"], valores_iguales,
                #                       "En la media", "En la media")
                #
