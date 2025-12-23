import plotly.graph_objects as go

from typing import Union

from config.constants_colors import COLORS, HOVER_BAR_TANSF_COLOR
from config.enums import SymbolEnum, DashEnum
from utils.exception_utils import execute_safely
from viewmodels.gomeria.transferencias_dep_vm import TransferenciasEntreDepositosVM
from viewmodels.plotly_components import HoverComponents, PlotComponents


class TransferenciasEntreDepositosPlotter:
    def __init__(self, cabecera: str) -> None:
        self.cabecera = cabecera
        self.df_transfer = TransferenciasEntreDepositosVM().get_df_by_cabecera(cabecera)
        self.hover = HoverComponents()
        self.plots = PlotComponents()

    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df_transfer.empty:
            df_2024 = self.df_transfer.loc[self.df_transfer["Año"] == 2024]
            df_2025 = self.df_transfer.loc[self.df_transfer["Año"] == 2025]

            x_2024 = df_2024["Repuesto"].to_list()
            y_2024 = df_2024["Cantidad"].to_numpy()

            x_2025 = df_2025["Repuesto"].to_list()
            y_2025 = df_2025["Cantidad"].to_numpy()

            fig = go.Figure()

            self.plots.scatter_gomeria(fig, x_2024, y_2024, "2024", COLORS[12], SymbolEnum.circle, DashEnum.solid)
            self.plots.scatter_gomeria(fig, x_2025, y_2025, "2025", COLORS[2], SymbolEnum.circle, DashEnum.dot)

            fig.update_xaxes(visible=False)
            fig.update_layout(
                showlegend=False,
                margin=dict(l=1, r=1, b=1, t=50),
                height=550,

                title = dict(text="🔛 Transferencias entre depósitos", y=0.98)
            )

            self.hover.hover_junto(fig)
            self.hover.color_hover_bar_colored(fig, HOVER_BAR_TANSF_COLOR)
            return fig
        return None