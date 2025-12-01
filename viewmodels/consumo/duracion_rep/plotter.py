from typing import Any, Tuple, List

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.constants_colors import DURACION_REPUESTOS_COLORS
from utils.exception_utils import execute_safely
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents
from viewmodels.consumo.duracion_rep.distri_normal_vm import DistribucionNormalVM
from viewmodels.consumo.duracion_rep.duracion_vm import DuracionRepuestosVM


class DuracionRepuestosPlotter:
    def __init__(self, repuesto: str):
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.df_duracion = DuracionRepuestosVM().get_df_by_repuesto(repuesto)
        self.df_distribucion = DistribucionNormalVM().get_df_by_repuesto(repuesto)

    def create_plot(self):
        fecha_min = self.df_duracion["FechaCambio"].min()
        fecha_max = self.df_duracion["FechaCambio"].max()
        cambios = self.df_distribucion["Cambio"].unique()
        rows: int = 2
        cols: int = 2
        titles: Tuple[str, ...] = ()
        specs: List[List[dict]] = []

        if rows == 2:
            specs = [[{"secondary_y": True}, {"secondary_y": True}],
                     [{"secondary_y": True}, {"secondary_y": True}]]
            titles = ("Cambio de 0KM", "Cambio 2", "Cambio 3", "Cambio 4")
        elif rows == 3:
            specs = [[{"secondary_y": True}, {"secondary_y": True}],
                     [{"secondary_y": True}, {"secondary_y": True}],
                     [{"secondary_y": True}, {"secondary_y": True}]]
            titles = ("Cambio de 0KM", "Cambio 2", "Cambio 3", "Cambio 4", "Cambio 5", "Cambio 6")

        fig = make_subplots(rows=rows, cols=cols, x_title="Duración en años", y_title="Frecuencia relativa en %",
                            horizontal_spacing=0.1, specs=specs, subplot_titles=titles)

        cambios_iter = iter(cambios)
        cambio = next(cambios_iter, None)
        colors = iter(DURACION_REPUESTOS_COLORS)

        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                df_distri_cambio = self.df_distribucion.loc[self.df_distribucion["Cambio"] == cambio]
                df_duracion_cambio = self.df_duracion.loc[self.df_duracion["Cambio"] == cambio]

                color_actual = next(colors)

                # Campana de gauss
                x = df_distri_cambio["Años"]
                y = df_distri_cambio["DistribucionNormal"]

                # Histograma
                data = df_duracion_cambio["DuracionEnAños"]

                fig.add_trace(go.Histogram(
                    x=data,
                    name="Frecuencia de aparición anual",
                    histnorm="percent",
                    nbinsx=10,
                    nbinsy=10,
                    opacity=0.4,
                    legendgroup=f"Cambio: {cambio}",
                    marker=dict(color=color_actual, opacity=0.5),

                    hoverinfo="skip",
                ), col=c, row=r, secondary_y=False)


                fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode="lines+markers",
                    name="Distribucion",
                    legendgroup=f"Cambio: {cambio}",
                    marker=dict(color=color_actual, opacity=1),
                    customdata=pd.Series(color_actual, x),

                    hovertemplate="""
<b>
<span style='color:white'>Duracion en años: %{x}</span>
</b>
<extra></extra>
""",
                    hoverlabel=dict(bgcolor=color_actual)  # ← color de la barra unified
                ), col=c, row=r, secondary_y=True)

                cambio = next(cambios_iter, None)

        fig.update_yaxes(title_text="", secondary_y=False) # Histograma
        fig.update_yaxes(title_text="Distribución en %", secondary_y=True) # Campana de gauss

        self.default.update_layout(fig, f"Duración repuestos ({fecha_min} | {fecha_max})",  height=725)

        fig.update_layout(
            barmode="overlay",
            showlegend=False,
            margin=dict(l=60, r=0, b=60, t=100),
        )

        self.hover.hover_x(fig)
        self.hover.color_hover_bar_subplot(fig)

        return fig


    @execute_safely
    def calcular_sin_cambios(self, year: str) -> Any:
        self.df_duracion["FechaCambio"] = pd.to_datetime(self.df_duracion["FechaCambio"], errors="coerce")
        year = pd.to_datetime(year, errors="coerce")

        df_year = self.df_duracion.loc[
                (self.df_duracion["FechaCambio"].dt.year == year.year) &
                (self.df_duracion["Cambio"] == 0)
        ]

        df_sin_cambios = self.df_duracion.loc[
            (self.df_duracion["Patente"].isin(df_year["Patente"])) &
            (self.df_duracion["Cambio"] == 1) &
            (self.df_duracion["FechaCambio"] == pd.to_datetime("2025-10-28")),
            ["Patente", "FechaCambio", "Cambio"]
        ]

        return df_sin_cambios.count().iat[0]