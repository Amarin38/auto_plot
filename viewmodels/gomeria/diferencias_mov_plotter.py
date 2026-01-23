import plotly.graph_objects as go

from typing import Union

from plotly.subplots import make_subplots

from config.constants_common import TITULOS_GOMERIA, ANCHO_COLS_GOMERIA, TICK_VALS_GOMERIA, TICK_TEXT_GOMERIA
from utils.exception_utils import execute_safely
from viewmodels.gomeria.diferencia_mov_dep_vm import DiferenciaMovimientosEntreDepositosVM
from viewmodels.plotly_components import HoverComponents, PlotComponents


class DiferenciaMovimientosEntreDepositosPlotter:
    def __init__(self) -> None:
        self.df = DiferenciaMovimientosEntreDepositosVM().get_df()
        self.plots = PlotComponents()

    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df.empty:
            df = self.df.set_index("Repuesto")

            df_costos       = df[["Costo2024", "Costo2025"]]
            df_consumos     = df[["Consumo2024", "Consumo2025"]]

            df_diferencias_consumos     = df[["Diferencia Consumos"]]
            df_diferencias_costos       = df[["Diferencia Costos"]]

            df_costos = df_costos.rename(
                columns={"Costo2024": "2024", "Costo2025": "2025"}
            )
            df_consumos = df_consumos.rename(
                columns={"Consumo2024": "2024", "Consumo2025": "2025"}
            )

            fig = make_subplots(
                cols=7, rows=1,
                subplot_titles=TITULOS_GOMERIA,
                column_widths=ANCHO_COLS_GOMERIA,
                shared_yaxes=True
            )

            # Posiciones relativas al gráfico
            pos_consumos                = fig.layout.xaxis.domain[1] + 0.001
            pos_costos                  = fig.layout.xaxis3.domain[1] + 0.001
            pos_diferencias_consumo     = fig.layout.xaxis5.domain[1] + 0.001
            pos_diferencias_costo       = fig.layout.xaxis7.domain[1] + 0.001

            self.plots.heat_map(fig, df_consumos, 1, 1, "Viridis", pos_consumos)
            self.plots.heat_map(fig, df_costos, 1, 3, "YlOrRd", pos_costos)
            self.plots.heat_map(fig, df_diferencias_consumos, 1, 5, "Viridis", pos_diferencias_consumo)
            self.plots.heat_map(fig, df_diferencias_costos, 1, 7, "YlOrRd", pos_diferencias_costo)

            fig.update_yaxes(tickfont=dict(size=13))
            fig.update_xaxes(tickmode="array", tickvals=TICK_VALS_GOMERIA, ticktext=TICK_TEXT_GOMERIA)
            fig.update_layout(
                margin=dict(l=1, r=1, b=1, t=70),
                height=700,
                width=900,
                title=dict(
                    text="ℹ️ Diferencias de movimientos",
                    y=0.98
                )

            )

            HoverComponents().hover_junto(fig)
            return fig
        return None



