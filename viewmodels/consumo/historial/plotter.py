import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.graph_objs import Figure

from config.enums_colors import HistorialColorsEnum
from config.enums import RepuestoEnum, TendenciaEnum
from utils.exception_utils import execute_safely
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, DropDownComponents, \
    HoverComponents
from viewmodels.consumo.historial.vm import HistorialConsumoVM


class HistorialPlotter:
    def __init__(self, tipo_rep: RepuestoEnum, tendencia: TendenciaEnum) -> None:
        self.tendencia = tendencia
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

                marker=dict(color=HistorialColorsEnum.VIOLETA),
                customdata=[HistorialColorsEnum.LILA] * len(x_data),
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
                y=self.calcular_tendencia(x_data, y_data, self.tendencia),
                mode="lines",
                name=f"Tendencia {self.tendencia}",
                line=dict(color=HistorialColorsEnum.VERDE, dash='dash'),
                hoverinfo="skip",
            ))

            fig.update_xaxes(tickmode="linear")

            self.default.update_layout(fig, f"{fecha_min} | {fecha_max}", "Año", "Historial de consumo")
            self.hover.hover_junto(fig)
            self.hover.color_hover_bar_colored(fig, HistorialColorsEnum.LILA)

            fig.update_layout(
                margin={"r": 0, "t": 55, "l": 0, "b": 0},
            )
            return fig, titulo
        return [None, None]

    @staticmethod
    @st.cache_data
    def calcular_tendencia(x_num: np.ndarray, y_data: np.ndarray, tendencia: TendenciaEnum) -> np.ndarray:
        coeficientes = None

        match tendencia:
            case TendenciaEnum.LINEAL: coeficientes = np.polyfit(x_num, y_data, 1)
            case TendenciaEnum.CUADRATICA: coeficientes = np.polyfit(x_num, y_data, 2)
            case TendenciaEnum.CUBICA: coeficientes = np.polyfit(x_num, y_data, 3)

        return np.polyval(coeficientes, x_num)