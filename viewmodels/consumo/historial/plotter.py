import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Figure

from config.constants_colors import COLORS
from config.enums import RepuestoEnum
from utils.exception_utils import execute_safely
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, DropDownComponents, \
    HoverComponents
from viewmodels.consumo.historial.vm import HistorialConsumoVM


class HistorialPlotter:
    def __init__(self, tipo_rep: RepuestoEnum) -> None:
        self.default = DefaultUpdateLayoutComponents()
        self.dropdown = DropDownComponents()
        self.hover = HoverComponents()

        self.tipo_rep = tipo_rep
        self.df = HistorialConsumoVM().get_df_tipo_repuesto(tipo_rep)


    @execute_safely
    def create_plot(self) -> tuple[Figure, str] | list[None]:
        if not self.df.empty:
            fecha_min = self.df["FechaMin"].unique()[0]
            fecha_max = self.df["FechaMax"].unique()[0]

            if self.tipo_rep:
                titulo = f"Historial {self.tipo_rep}"
            else:
                titulo = ""

            x_data = self.df["Año"]
            y_data = self.df["TotalConsumo"]

            x_num = np.arange(len(x_data))

            m, b = np.polyfit(x_num, y_data, 1)
            lineal_y = m * x_num + b

            a, b, c = np.polyfit(x_num, y_data, 2)
            cuadratica_y = a * x_num **2 + b * x_num + c

            a, b, c, d = np.polyfit(x_num, y_data, 3)
            cubica_y = a * x_num **3 + b * x_num **2 + c * x_num + d


            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x_data,
                y=y_data,
                name="Historial de consumo",

                textposition="auto",
                textfont=dict(
                    size=11,
                    color='white',
                    family='Arial'
                ),

                marker=dict(color=COLORS[10]),
                customdata=pd.Series(COLORS[15], x_data),
                hovertemplate="""
<b>
<span style='color:%{customdata}; font-size:15px'>Consumo:</span>
%{y:.0f}
</b>
<extra></extra>
"""
            ))


            fig.add_trace(go.Scatter(
                x=x_data,
                y=lineal_y,
                mode="lines",
                name=f"Tendencia",
                line=dict(color=COLORS[12], dash='dash'),
                visible=True,
                hoverinfo="skip",
            ))

            fig.add_trace(go.Scatter(
                x=x_data,
                y=cuadratica_y,
                mode="lines",
                name=f"Tendencia",
                line=dict(color=COLORS[8], dash='dash'),
                visible=False,
                hoverinfo="skip",
            ))

            fig.add_trace(go.Scatter(
                x=x_data,
                y=cubica_y,
                mode="lines",
                name=f"Tendencia",
                line=dict(color=COLORS[7], dash='dash'),
                visible=False,
                hoverinfo="skip",
            ))

            fig.update_xaxes(tickmode="linear")

            self.default.update_layout(fig, f"{fecha_min} | {fecha_max}", "Año", "Historial de consumo")
            self.dropdown.dropdown(fig, [
                dict(
                    label="Lineal",
                    method="update",
                    args=[{"visible": [True, True, False, False]}],
                ),
                dict(
                    label="Cuadrática",
                    method="update",
                    args=[{"visible": [True, False, True, False]}],
                ),
                dict(
                    label="Cúbica",
                    method="update",
                    args=[{"visible": [True, False, False, True]}],
                )
            ])
            self.hover.hover_junto(fig)
            self.hover.color_hover_bar(fig, COLORS[15])

            return fig, titulo
        return [None, None]