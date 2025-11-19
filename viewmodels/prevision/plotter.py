import pandas as pd

import plotly.graph_objects as go

from config.constants import COLORS, FILE_STRFTIME_YMD

from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout, devolver_fecha, range_slider, top_right_legend, hover_unified, \
    hover_separado

from viewmodels.prevision.data_vm import PrevisionDataVM
from viewmodels.prevision.vm import PrevisionVM


class ForecastPlotter:
    def __init__(self, tipo_rep: str):
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
                titulo = f'Prevision de {self.tipo_rep} ({devolver_fecha(self.df_data, "FechaCompleta")})'
            else:
                titulo = ""

            for repuesto in todos_repuestos:
                x_data = self.df_data.loc[self.df_data['Repuesto'] == repuesto, 'FechaCompleta']
                y_data = self.df_data.loc[self.df_data['Repuesto'] == repuesto, 'Consumo']

                x_forecast = self.df_forecast.loc[self.df_forecast['Repuesto'] == repuesto, 'FechaCompleta']
                y_forecast = self.df_forecast.loc[self.df_forecast['Repuesto'] == repuesto, 'Prevision']

                total_prevision = y_forecast.sum()
                valor_mensual = int(y_forecast.mean())

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data,
                    name='Consumo',
                    mode='lines+markers+text',

                    text=y_data,
                    textposition='top center',
                    textfont=dict(
                        size=19,
                        color=COLORS[15]
                    ),

                    line=dict(color=COLORS[16], width=2),
                    marker=dict(
                        color=COLORS[16],
                        size=8,
                        symbol='circle',
                    ),
                    legendgroup="Consumo",
                    hovertemplate="""
<b>
<span style='color:red'></span>
</b>%{y}
<extra></extra>
"""
                ))


                fig.add_trace(go.Scatter(
                    x=x_forecast,
                    y=y_forecast,
                    name=f'Prevision',
                    mode='lines+markers+text',

                    text=y_forecast,
                    textposition='top center',
                    textfont=dict(
                        size=19,
                        color=COLORS[1]
                    ),

                    line=dict(color=COLORS[3], width=2, dash='dash'),
                    marker=dict(
                        color=COLORS[3],
                        size=8,
                        symbol='square',
                    ),
                    legendgroup="Prevision",
                    hovertemplate="""
<b>
<span style='color:green'></span>
</b>%{y}
<extra></extra>
"""
                ))

                fig.add_trace(go.Scatter(
                    x=[None],  # nada visible
                    y=[None],
                    mode="markers",
                    marker=dict(color="rgba(0,0,0,0)"),  # transparente
                    showlegend=True,
                    name=f"Prevision total: {total_prevision}",
                    legendgroup="Prevision"
                ))

                fig.add_trace(go.Scatter(
                    x=[None],  # nada visible
                    y=[None],
                    mode="markers",
                    marker=dict(color="rgba(0,0,0,0)"),  # transparente
                    showlegend=True,
                    name=f"Valor por mes: {valor_mensual}",
                    legendgroup="Prevision"
                ))


                update_layout(fig, repuesto, "Fecha", "Consumo")
                range_slider(fig)
                top_right_legend(fig)
                hover_separado(fig)

                figuras.append(fig)
            return figuras, titulo
        return [None, None]
