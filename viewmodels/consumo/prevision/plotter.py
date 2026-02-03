import streamlit as st
import pandas as pd
from babel.dates import format_date

import plotly.graph_objects as go

from config.enums_colors import PrevisionColorsEnum
from config.constants_common import FILE_STRFTIME_YMD
from config.enums import SymbolEnum, DashEnum

from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents, SliderComponents, \
    PlotComponents

from viewmodels.consumo.prevision.data_vm import PrevisionDataVM
from viewmodels.consumo.prevision.vm import PrevisionVM



class PrevisionPlotter:
    def __init__(self, tipo_rep: str):
        self.common = CommonUtils()
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.slider = SliderComponents()
        self.plots = PlotComponents()

        self.tipo_rep = tipo_rep
        self.df_data = PrevisionDataVM().get_df_by_tipo_repuesto(self.tipo_rep)
        self.df_forecast = PrevisionVM().get_df_by_tipo_repuesto(self.tipo_rep)
        self.fecha = self.common.devolver_fecha(self.df_data, "FechaCompleta")

    @execute_safely
    def create_plot(self):
        if not self.df_data.empty and not self.df_forecast.empty:
            figuras = []
            todos_repuestos = self.df_data['Repuesto'].unique()

            self.df_data['FechaCompleta'] = pd.to_datetime(self.df_data['FechaCompleta'], format=FILE_STRFTIME_YMD)
            self.df_forecast['FechaCompleta'] = pd.to_datetime(self.df_forecast['FechaCompleta'], format=FILE_STRFTIME_YMD)

            titulo = f'ConsumoPrevision de {self.tipo_rep} ({self.fecha})' if self.tipo_rep else ""

            grupos_data = self.df_data.groupby('Repuesto')
            grupos_forecast = self.df_forecast.groupby('Repuesto')

            for repuesto in todos_repuestos:
                df_rep_data = grupos_data.get_group(repuesto) # separo por el repuesto actual
                df_rep_forecast = grupos_forecast.get_group(repuesto)

                x_data = df_rep_data['FechaCompleta']
                y_data = df_rep_data['Consumo'].to_numpy()

                x_forecast = df_rep_forecast['FechaCompleta']
                y_forecast = df_rep_forecast['ConsumoPrevision'].to_numpy()

                total_prevision = y_forecast.sum()
                valor_mensual = int(y_forecast.mean())

                # Ticks
                ticks_text_data = calcular_ticks(x_data)
                ticks_text_forecast = calcular_ticks(x_forecast)

                tickvals = pd.concat([x_data, x_forecast]).reset_index(drop=True) # type: ignore
                ticktext = pd.concat([ticks_text_data, ticks_text_forecast]).reset_index(drop=True)

                fig = go.Figure()

                self.plots.scatter_prevision(fig, x_data, y_data, "Consumo",
                                             PrevisionColorsEnum.LILA, PrevisionColorsEnum.VIOLETA,
                                             SymbolEnum.CIRCLE, DashEnum.SOLID, ticks_text_data)

                self.plots.scatter_prevision(fig, x_forecast, y_forecast, "Prevision",
                                             PrevisionColorsEnum.NARANJA_FUERTE, PrevisionColorsEnum.NARANJA,
                                             SymbolEnum.SQUARE, DashEnum.DASH, ticks_text_forecast)

                self.plots.empty(fig, f"Prevision total: {total_prevision}")
                self.plots.empty(fig, f"Valor por mes: {valor_mensual}")

                step = 3
                ticktext_all = [
                    ticktext[i]
                    if i % step == 0
                    else ""  # Dejar vacío NO borra el tick
                    for i in range(len(ticktext))
                ]

                self.default.update_layout(fig, repuesto, "Fecha", "Consumo")
                self.slider.range_slider(fig)

                self.hover.hover_x(fig)
                self.hover.tick_array(fig, tickvals, ticktext_all)
                self.hover.color_hover_bar(fig)

                figuras.append(fig)
            return figuras, titulo
        return [None, None]

@st.cache_data
def calcular_ticks(x):
    año = x.apply(
        lambda d: format_date(d, "MMM", locale="es").capitalize()
    )
    mes = x.dt.strftime("%Y")
    return año + ", " + mes