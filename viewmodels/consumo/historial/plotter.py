import numpy as np
import streamlit as st
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
            fecha_min = self.df["FechaMin"].iloc()[0]
            fecha_max = self.df["FechaMax"].iloc()[0]

            titulo = f"Historial {self.tipo_rep}" if self.tipo_rep else ""

            x_data = self.df["Año"].to_numpy()
            y_data = self.df["TotalConsumo"].to_numpy()

            lineal_y = calcular_tendencia(x_data, y_data, 1)

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
                customdata=[COLORS[15]] * len(x_data),
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
                y=calcular_tendencia(x_data, y_data, 2),
                mode="lines",
                name=f"Tendencia",
                line=dict(color=COLORS[8], dash='dash'),
                visible=False,
                hoverinfo="skip",
            ))

            fig.add_trace(go.Scatter(
                x=x_data,
                y=calcular_tendencia(x_data, y_data, 3),
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
            self.hover.color_hover_bar_colored(fig, COLORS[15])

            return fig, titulo
        return [None, None]

@st.cache_data
def calcular_tendencia(x_num: np.ndarray, y_data: np.ndarray, grado: int) -> np.ndarray:
    coeficientes = np.polyfit(x_num, y_data, grado)
    return np.polyval(coeficientes, x_num)