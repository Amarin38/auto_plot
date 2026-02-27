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


def _generar_columna_ticks(serie_fechas):
    fechas_unicas = serie_fechas.unique()

    mapa_fechas = {
        fecha: f"{format_date(fecha, 'MMM', locale='es').capitalize()}, {fecha.year}"
        for fecha in fechas_unicas
    }
    return serie_fechas.map(mapa_fechas)


class PrevisionPlotter:
    def __init__(self, df_data: pd.DataFrame, df_forecast: pd.DataFrame, tipo_rep: str):
        self.common = CommonUtils()
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.slider = SliderComponents()
        self.plots = PlotComponents()

        self.tipo_rep = tipo_rep
        self.df_data = df_data
        self.df_forecast = df_forecast

        if not self.df_data.empty:
            self.df_data['FechaCompleta'] = pd.to_datetime(self.df_data['FechaCompleta'], format=FILE_STRFTIME_YMD)
            self.fecha = self.common.devolver_fecha(self.df_data, "FechaCompleta")

        if not self.df_forecast.empty:
            self.df_forecast['FechaCompleta'] = pd.to_datetime(self.df_forecast['FechaCompleta'], format=FILE_STRFTIME_YMD)


    @execute_safely
    def create_plot(self):
        if not self.df_data.empty and not self.df_forecast.empty:
            figuras = []
            todos_repuestos = self.df_data['Repuesto'].unique()

            titulo = f'Prevision de {self.tipo_rep} ({self.fecha})' if self.tipo_rep else ""

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
                ticks_text_data = _generar_columna_ticks(x_data)
                ticks_text_forecast = _generar_columna_ticks(x_forecast)

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

