import pandas as pd
import plotly.graph_objects as go

from typing import Union

from plotly.subplots import make_subplots

from config.constants_views import TITULOS_GOMERIA, ANCHO_COLS_GOMERIA, TICK_VALS_GOMERIA, TICK_TEXT_GOMERIA
from config.enums_colors import HoverColorsEnum, TransferEntreDepoColorsEnum
from config.enums import SymbolEnum, DashEnum
from viewmodels.plotly_components import HoverComponents, PlotComponents


class TransferenciasEntreDepositosPlotter:
    def __init__(self) -> None:
        self.hover = HoverComponents()
        self.plots = PlotComponents()

    def create_transferencias_plot(self, df_transfer: pd.DataFrame) -> Union[go.Figure, None]:
        if df_transfer.empty:
            return None

        df_2024 = df_transfer.loc[df_transfer["Año"] == 2024]
        df_2025 = df_transfer.loc[df_transfer["Año"] == 2025]

        x_2024 = df_2024["Repuesto"].to_list()
        y_2024 = df_2024["Cantidad"].to_numpy()

        x_2025 = df_2025["Repuesto"].to_list()
        y_2025 = df_2025["Cantidad"].to_numpy()

        fig = go.Figure()

        self.plots.scatter_gomeria(
            fig,
            x_2024,
            y_2024,
            "2024",
            TransferEntreDepoColorsEnum.AZUL,
            SymbolEnum.CIRCLE,
            DashEnum.SOLID
        )

        self.plots.scatter_gomeria(
            fig,
            x_2025,
            y_2025,
            "2025",
            TransferEntreDepoColorsEnum.ROJO,
            SymbolEnum.CIRCLE,
            DashEnum.DOT
        )

        fig.update_xaxes(visible=False)
        fig.update_layout(
            showlegend=False,
            margin=dict(l=1, r=1, b=1, t=50),
            height=550,

            title = dict(text="🔛 Transferencias entre depósitos", y=0.98)
        )

        self.hover.hover_junto(fig)
        self.hover.color_hover_bar_colored(fig, HoverColorsEnum.VIOLETA)
        return fig


    def create_diferencia_plot(self, df_difer: pd.DataFrame) -> Union[go.Figure, None]:
        if df_difer.empty:
            return None

        df = df_difer.set_index("Repuesto")

        df = df.fillna(0)

        df_costos       = df[["CostoTotal2024", "CostoTotal2025"]]
        df_consumos     = df[["Cantidad2024", "Cantidad2025"]]

        df_diferencias_consumos     = df[["DiferenciaAnual"]]
        df_diferencias_costos       = df[["DiferenciaDeCostos"]]

        df_costos = df_costos.rename(
            columns={"CostoTotal2024": "2024", "CostoTotal2025": "2025"}
        )
        df_consumos = df_consumos.rename(
            columns={"Cantidad2024": "2024", "Cantidad2025": "2025"}
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

        self.plots.heat_map(
            fig,
            df_consumos,
            1,
            1,
            "Viridis",
            pos_consumos
        )

        self.plots.heat_map(
            fig,
            df_costos,
            1,
            3,
            "YlOrRd",
            pos_costos
        )

        self.plots.heat_map(
            fig,
            df_diferencias_consumos,
            1,
            5,
            "Viridis",
            pos_diferencias_consumo
        )

        self.plots.heat_map(
            fig,
            df_diferencias_costos,
            1,
            7,
            "YlOrRd",
            pos_diferencias_costo
        )

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

        self.hover.hover_junto(fig)
        return fig
