from typing import Any, Tuple, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit
from pandas import Series
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots
from itertools import product

from config.enums import PeriodoComparacionEnum, ConsumoComparacionRepuestoEnum, CabecerasEnum
from config.enums_colors import DuracionRepuestosColorsEnum, IndiceColorsEnum, DuracionRepuestosColorsEnum, \
    ConsumoComparacionOscuroColorsEnum
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
            titulo      = f"Comparación: {self.cabecera}"
            agrupado    = (self.df
                           .groupby(["Cabecera", "TipoRepuesto", "PeriodoID", "FechaTitulo"])
                           .agg({"Consumo":"sum"})
                           .reset_index())

            fig = go.Figure()

            periodos_unicos = sorted(agrupado["PeriodoID"].unique(), reverse=False)

            for periodo, color, color_fecha in zip(periodos_unicos,
                                                   DuracionRepuestosColorsEnum.as_list(),
                                                   ConsumoComparacionOscuroColorsEnum.as_list()):
                datos_periodo = agrupado[agrupado["PeriodoID"] == periodo]

                x = datos_periodo["TipoRepuesto"]
                y = datos_periodo["Consumo"]
                fechas = datos_periodo["FechaTitulo"]
                size_x = len(x)

                custom_data = np.stack((
                                y,
                               [str(periodo)] * size_x,
                               [color] * size_x,
                               [color_fecha] * size_x,
                               fechas
                               ), axis=-1)

                fig.add_trace(go.Bar(
                    x=x,
                    y=y.to_numpy(),
                    name=str(periodo),
                    textposition="inside",
                    textfont=dict(
                        size=13,
                        color='white',
                        family='Arial'
                    ),
                    customdata=custom_data,
                    marker=dict(color=color),
                    hovertemplate="""
<b>
<span style='color:%{customdata[2]}'>%{customdata[1]}:</span>
</b>
%{customdata[0]:.0f} (%{y:.0f}%)<br>
<span style='color:%{customdata[3]}'>   <b>•  %{customdata[4]}</b></span>
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
