from typing import Any, Tuple, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pandas import Series
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots
from itertools import product

from config.enums import PeriodoComparacionEnum, ConsumoComparacionRepuestoEnum, CabecerasEnum
from config.enums_colors import DuracionRepuestosColorsEnum, IndiceColorsEnum, DuracionRepuestosColorsEnum
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
            titulo = f"Comparación: {self.cabecera}"
            agrupado = self.df.groupby(["Cabecera", "TipoRepuesto", "PeriodoID"]).agg({"Consumo":"sum"}).reset_index()

            fig = go.Figure()

            periodos_unicos = sorted(agrupado["PeriodoID"].unique(), reverse=False)

            for periodo, color in zip(periodos_unicos, DuracionRepuestosColorsEnum.as_list()):
                datos_periodo = agrupado[agrupado["PeriodoID"] == periodo]

                x = datos_periodo["TipoRepuesto"]
                y = datos_periodo["Consumo"]

                cd = np.stack((y, [str(periodo)] * len(x), [color] * len(x)), axis=-1)

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
<span style='color:%{customdata[2]}'>%{customdata[1]}:</span>
</b>
%{customdata[0]:.0f} (%{y:.0f}%)
<extra></extra>
"""
                                ))

            fig.update_layout(
                title=titulo,
                xaxis_title="Tipo de Repuesto",
                xaxis={
                    'categoryorder': 'array',
                    'categoryarray': PeriodoComparacionEnum.as_list()
                },
                legend_title="Periodos",
                barmode='group',
                barnorm='percent',  # Esto estira ambos periodos al mismo techo (100%)
                yaxis_title="Proporción del Consumo (%)",
                height=564,
                margin = {"r": 0, "t": 40, "l": 0, "b": 0},

            )
            self.hover.hover_junto(fig)

            return fig if fig else None
        return None
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
