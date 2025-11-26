import pandas as pd
from babel.dates import format_date

import plotly.graph_objects as go

from config.constants import COLORS, FILE_STRFTIME_YMD

from utils.exception_utils import execute_safely
from utils.common_utils import CommonUtils
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents, SliderComponents, \
    ScatterComponents

from viewmodels.consumo.prevision.data_vm import PrevisionDataVM
from viewmodels.consumo.prevision.vm import PrevisionVM




class PrevisionPlotter:
    def __init__(self, tipo_rep: str):
        self.common = CommonUtils()
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.slider = SliderComponents()
        self.scatter = ScatterComponents()

        self.tipo_rep = tipo_rep
        self.df_data = PrevisionDataVM().get_df_by_tipo_repuesto(self.tipo_rep)
        self.df_forecast = PrevisionVM().get_df_by_tipo_repuesto(self.tipo_rep)


    @execute_safely
    def create_plot(self):
        if not self.df_data.empty and not self.df_forecast.empty:
            figuras = []
            todos_repuestos = self.df_data['Repuesto'].unique()

            self.df_data['FechaCompleta'] = pd.to_datetime(self.df_data['FechaCompleta'], format=FILE_STRFTIME_YMD)
            self.df_forecast['FechaCompleta'] = pd.to_datetime(self.df_forecast['FechaCompleta'], format=FILE_STRFTIME_YMD)

            if self.tipo_rep:
                titulo = f'ConsumoPrevision de {self.tipo_rep} ({self.common.devolver_fecha(self.df_data, "FechaCompleta")})'
            else:
                titulo = ""

            for repuesto in todos_repuestos:
                x_data = self.df_data.loc[self.df_data['Repuesto'] == repuesto, 'FechaCompleta']
                y_data = self.df_data.loc[self.df_data['Repuesto'] == repuesto, 'Consumo']

                x_forecast = self.df_forecast.loc[self.df_forecast['Repuesto'] == repuesto, 'FechaCompleta']
                y_forecast = self.df_forecast.loc[self.df_forecast['Repuesto'] == repuesto, 'ConsumoPrevision']

                total_prevision = y_forecast.sum()
                valor_mensual = int(y_forecast.mean())

                # Ticks para datos reales
                x_data_year = x_data.apply(lambda d: format_date(d, "MMM", locale="es").capitalize() + ", ")
                x_data_month = x_data.dt.strftime("%Y")
                x_data_new = x_data_year + x_data_month

                # Ticks para forecast
                x_forecast_year = x_forecast.apply(lambda d: format_date(d, "MMM", locale="es").capitalize() + ", ")
                x_forecast_month = x_forecast.dt.strftime("%Y")
                x_forecast_new = x_forecast_year + x_forecast_month


                tickvals = pd.concat([x_data, x_forecast]).reset_index(drop=True) # type: ignore
                ticktext = pd.concat([x_data_new, x_forecast_new]).reset_index(drop=True)


                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data,
                    name='Consumo',
                    mode='lines+markers',

                    text=y_data,
                    textposition='top center',
                    textfont=dict(
                        size=19,
                        color=COLORS[15]
                    ),

                    line=dict(color="#485696", width=2),
                    marker=dict(
                        color="#485696",
                        size=8,
                        symbol='circle',
                    ),
                    legendgroup="Consumo",
                    customdata=x_data_new,
                    hovertemplate="""
<b>
<span style='color:#485696'>Consumo:</span>
</b> %{y}
<extra></extra>
""",
                ))


                fig.add_trace(go.Scatter(
                    x=x_forecast,
                    y=y_forecast,
                    name=f'Prevision',
                    mode='lines+markers',

                    text=y_forecast,
                    textposition='top center',
                    textfont=dict(
                        size=19,
                        color=COLORS[1]
                    ),

                    line=dict(color="#F24C00", width=2, dash='dash'),
                    marker=dict(
                        color="#F24C00",
                        size=8,
                        symbol='square',
                    ),
                    legendgroup="ConsumoPrevision",
                    customdata=x_forecast_new,
                    hoverinfo="skip",
                    hovertemplate="""
<b><span style='color:#F24C00'>Prevision:</span></b> %{y}
<extra></extra>
"""
                ))

                self.scatter.empty(fig, f"Prevision total: {total_prevision}")
                self.scatter.empty(fig, f"Valor por mes: {valor_mensual}")

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
                self.hover.color_hover_bar(fig, "white")

                figuras.append(fig)
            return figuras, titulo
        return [None, None]
