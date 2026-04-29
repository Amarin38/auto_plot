import pandas as pd

import plotly.graph_objects as go

from config.constants_common import PAGE_STRFTIME_DMY, FILE_STRFTIME_YMD
from config.enums_colors import PrevisionColorsEnum
from config.enums import SymbolEnum, DashEnum

from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents, SliderComponents, \
    PlotComponents, _generar_columna_ticks_español


class PrevisionPlotter:
    def __init__(self, df_data: pd.DataFrame, df_forecast: pd.DataFrame, df_stock: pd.DataFrame, tipo_rep: str):
        self.common = CommonUtils()
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.slider = SliderComponents()
        self.plots = PlotComponents()

        self.tipo_rep = tipo_rep
        self.df_stock = df_stock
        self.df_data = df_data
        self.df_forecast = df_forecast

        if not self.df_data.empty:
            self.fecha = self.common.devolver_fecha(self.df_data, "Mes")

    @execute_safely
    def create_plot(self):
        if not self.df_data.empty and not self.df_forecast.empty:
            self.df_data['Mes'] = pd.to_datetime(self.df_data['Mes'],
                                                 format=PAGE_STRFTIME_DMY,
                                                 errors="coerce")
            self.df_forecast['FechaPrevision'] = pd.to_datetime(self.df_forecast['FechaPrevision'],
                                                                format=FILE_STRFTIME_YMD,
                                                                errors="coerce")

            # Forzamos números para el Eje Y
            self.df_data['ConsumoMensual'] = pd.to_numeric(self.df_data['ConsumoMensual'], errors="coerce")
            self.df_forecast['Prevision'] = pd.to_numeric(self.df_forecast['Prevision'], errors="coerce")

            # Limpiamos errores de conversión
            self.df_data = self.df_data.dropna(subset=['Mes', 'ConsumoMensual'])
            self.df_forecast = self.df_forecast.dropna(subset=['FechaPrevision', 'Prevision'])
            # --------------------------------

            figuras = []
            todos_repuestos = self.df_data['Articulo'].unique()

            titulo = f'Prevision de {self.tipo_rep} ({self.fecha})' if self.tipo_rep else ""

            grupos_data = self.df_data.groupby('Articulo')
            grupos_forecast = self.df_forecast.groupby('RepuestoPrevision')
            grupos_stock = self.df_stock.groupby("RepuestoStock")

            for repuesto in todos_repuestos:
                try:
                    df_rep_data = grupos_data.get_group(repuesto)
                    df_rep_forecast = grupos_forecast.get_group(repuesto)
                    df_rep_stock = grupos_stock.get_group(repuesto)
                except KeyError:
                    continue

                x_data = df_rep_data['Mes']
                y_data = df_rep_data['ConsumoMensual'].to_numpy()

                x_forecast = df_rep_forecast['FechaPrevision']
                y_forecast = df_rep_forecast['Prevision'].to_numpy()
                y_forecast_stock = df_rep_forecast['RestoStock'].to_numpy()

                total_prevision = y_forecast.sum()
                valor_mensual = int(y_forecast.mean())

                # Ticks
                ticks_text_data = _generar_columna_ticks_español(x_data)
                ticks_text_forecast = _generar_columna_ticks_español(x_forecast)

                tickvals = pd.concat([x_data, x_forecast]).reset_index(drop=True)  # type: ignore
                ticktext = pd.concat([ticks_text_data, ticks_text_forecast]).reset_index(drop=True)

                fig = go.Figure()

                self.plots.scatter_prevision(fig, x_data, y_data, "ConsumoMensual",
                                             PrevisionColorsEnum.LILA, PrevisionColorsEnum.VIOLETA,
                                             SymbolEnum.CIRCLE, DashEnum.SOLID, ticks_text_data, "")

                self.plots.scatter_prevision(fig, x_forecast, y_forecast, "Prevision",
                                             PrevisionColorsEnum.NARANJA_FUERTE, PrevisionColorsEnum.NARANJA,
                                             SymbolEnum.SQUARE, DashEnum.DASH, ticks_text_forecast, "")

                self.plots.scatter_prevision(fig, x_forecast, y_forecast_stock, "RestoStock",
                                             PrevisionColorsEnum.VERDE, PrevisionColorsEnum.VERDE_CLARO,
                                             SymbolEnum.CIRCLE, DashEnum.DOT, ticks_text_forecast, df_rep_stock["FechaStock"].iloc[0])

                fig.add_hline(
                    y=0,
                    line_dash="solid",
                    line_color="#666666",
                    line_width=2,
                    annotation_text="0",
                    annotation_position="bottom right"
                )

                self.plots.empty(fig, f"Prevision total: {total_prevision}")
                self.plots.empty(fig, f"Valor por mes: {valor_mensual}")

                step = 3
                ticktext_all = [
                    ticktext[i]
                    if i % step == 0
                    else ""
                    for i in range(len(ticktext))
                ]

                self.default.update_layout(fig, repuesto, "Fecha", "Consumo")
                self.slider.range_slider(fig, x_data.mean(), x_forecast.max())

                self.hover.hover_x(fig)
                self.hover.tick_array(fig, tickvals, ticktext_all)
                self.hover.color_hover_bar(fig)

                figuras.append(fig)

            return figuras, titulo

        return [None, None]

