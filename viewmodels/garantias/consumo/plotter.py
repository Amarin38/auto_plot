from typing import Union

import pandas as pd
import plotly.graph_objects as go

from config.enums_colors import ConsumoGarantiasColorsEnum
from utils.exception_utils import execute_safely
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents, PlotComponents


class ConsumoGarantiasPlotter:
    def __init__(self, df: pd.DataFrame):
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.plots = PlotComponents()

        self.df_data = df


    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df_data.empty:
            x_data              = self.df_data["Repuesto"]
            y_garantias         = self.df_data["Garantia"].to_numpy()
            y_transfer          = self.df_data["Transferencia"].to_numpy()
            diferencia_gar      = self.df_data["PorcentajeGarantia"]
            diferencia_transfer = self.df_data["PorcentajeTransferencia"]


            color_garantias = ConsumoGarantiasColorsEnum.ROJO
            color_transferencias = ConsumoGarantiasColorsEnum.VERDE

            len_data = len(x_data)

            custom_garantias = list(zip(
                ["Garantias"] * len_data,
                [color_garantias] * len_data
            ))

            custom_transferencias = list(zip(
                ["Transferencias"] * len_data,
                [color_transferencias] * len_data
            ))

            fig = go.Figure()

            self.plots.bar_indice_consumo(fig, x_data, y_garantias, "Garantias", diferencia_gar, color_garantias, custom_garantias)
            self.plots.bar_indice_consumo(fig, x_data, y_transfer, "Transferencia", diferencia_transfer, color_transferencias, custom_transferencias)

            self.default.update_layout(fig,'Consumo garantias frente a transferencias', 'Repuesto', 'Consumo', height=665)
            self.hover.hover_junto(fig)

            fig.update_layout(
                showlegend=False,
            )

            return fig
        return None