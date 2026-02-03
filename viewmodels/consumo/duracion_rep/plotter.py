from typing import Any, Tuple, List

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import product

from config.constants_colors import DURACION_REPUESTOS_COLORS
from config.constants_common import FILE_STRFTIME_YMD
from utils.exception_utils import execute_safely
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents
from viewmodels.consumo.duracion_rep.distri_normal_vm import DistribucionNormalVM
from viewmodels.consumo.duracion_rep.duracion_vm import DuracionRepuestosVM


class DuracionRepuestosPlotter:
    def __init__(self, repuesto: str, rows: int):
        self.rows               = rows
        self.cols               = 2
        self.hover              = HoverComponents()
        self.default            = DefaultUpdateLayoutComponents()
        self.df_duracion        = DuracionRepuestosVM().get_df_by_repuesto(repuesto)
        self.df_distribucion    = DistribucionNormalVM().get_df_by_repuesto(repuesto)

        self.df_duracion["FechaCambio"] = pd.to_datetime(
            self.df_duracion["FechaCambio"], errors="coerce"
        )

    def create_plot(self):
        fecha_min   = self.df_duracion["FechaCambio"].min().strftime(FILE_STRFTIME_YMD)
        fecha_max   = self.df_duracion["FechaCambio"].max().strftime(FILE_STRFTIME_YMD)
        cambios     = self.df_distribucion["Cambio"].unique()
        positions = list(product(range(1, self.rows + 1), range(1, self.cols + 1)))
        specs = [[{"secondary_y": True}, {"secondary_y": True}] for _ in range(self.rows)]
        titles = ["Cambio de 0KM"]
        titles.extend(f"Cambio {i}" for i in range(2, 2 * len(specs) + 1))


        fig = make_subplots(rows=self.rows, cols=self.cols, x_title="Duración en años", y_title="Frecuencia relativa en %",
                            horizontal_spacing=0.1, specs=specs, subplot_titles=titles)


        df_distri_cambio = self.df_distribucion.groupby("Cambio")
        df_duracion_cambio = self.df_duracion.groupby("Cambio")

        for (row, col), cambio, color_actual in zip(positions, cambios, DURACION_REPUESTOS_COLORS):
                df_distri = df_distri_cambio.get_group(cambio)
                df_duracion = df_duracion_cambio.get_group(cambio)

                # Campana de gauss
                x = df_distri["Años"].to_numpy()
                y = df_distri["DistribucionNormal"].to_numpy()

                # Histograma
                data = df_duracion["DuracionEnAños"].to_numpy()

                fig.add_trace(go.Histogram(
                    x=data,
                    name="Frecuencia de aparición anual",
                    histnorm="percent",
                    nbinsx=10,
                    opacity=0.4,
                    legendgroup=f"Cambio: {cambio}",
                    marker=dict(color=color_actual, opacity=0.5),
                    hoverinfo="skip",
                ), col=col, row=row, secondary_y=False)

                fig.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode="lines+markers",
                    name="Distribucion",
                    legendgroup=f"Cambio: {cambio}",
                    marker=dict(color=color_actual, opacity=1),
                    customdata=[color_actual] * len(x),
                    hovertemplate="""
<b>
<span style='color:white'>Duracion en años: %{x}</span>
</b>
<extra></extra>
""",
                    hoverlabel=dict(bgcolor=color_actual)  # ← color de la barra unified
                ), col=col, row=row, secondary_y=True)


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
    def calcular_sin_cambios(self, year_str: str) -> Any:
        year = pd.to_datetime(year_str, errors="coerce")

        df_year = self.df_duracion.loc[
                (self.df_duracion["FechaCambio"].dt.year == year.year) &
                (self.df_duracion["Cambio"] == 0),
                ["Patente"]
        ]

        df_sin_cambios = (
             self.df_duracion
            .merge(df_year, on="Patente", how="inner")
            .loc[
                (self.df_duracion["Cambio"] == 1) &
                (self.df_duracion["FechaCambio"] == pd.Timestamp("2025-10-28"))
            ]
        )

        return df_sin_cambios.count().iat[0]