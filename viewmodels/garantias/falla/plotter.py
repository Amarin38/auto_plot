from typing import Union

import pandas as pd
import plotly.graph_objects as go

from config.constants_views import PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH, PIE_FONT_SIZE
from config.enums_colors import FallaGarantiasColorsEnum, ConsumoGarantiasColorsEnum

from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents, PlotComponents


class FallaGarantiasPlotter:
    def __init__(self, min_date: str = "", max_date: str = "") -> None:
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.plots = PlotComponents()
        self.min_date = min_date
        self.max_date = max_date

    def create_falla_plot(self, df_data: pd.DataFrame) -> Union[go.Figure, None]:
        labels  = df_data["Repuesto"]
        values  = df_data["PromedioTiempoFalla"].to_numpy()
        text    = df_data["PromedioTiempoFalla"].astype(str)

        fig = go.Figure()

        fig.add_trace(go.Pie(
                labels=labels,
                values=values,
                text=text,
                textfont=dict(
                    size=PIE_FONT_SIZE
                ),
                name='Fallas',
                insidetextorientation='horizontal',
                textposition='auto',
                customdata=FallaGarantiasColorsEnum.as_list(),
                marker=dict(colors=FallaGarantiasColorsEnum.as_list()),
                hovertemplate="""
<b>
<span style='color:%{customdata}'>%{label}</span><br>
<span style='color:white'>%{text} (%{percent})</span>
</b>
<extra></extra>
""",
        ))

        fig.update_traces(
            hoverinfo='label+value+percent',
            textinfo='percent',
            showlegend=False,
        )

        self.default.update_layout(
            fig,
            f'Fallos ({self.min_date} - {self.max_date})',
            '',
            '',
            PIE_PLOT_HEIGHT,
            PIE_PLOT_WIDTH
        )

        self.hover.hover_x(fig)
        return fig


    def create_consumo_plot(self, df_data: pd.DataFrame) -> Union[go.Figure, None]:
        if df_data.empty:
            return None

        x_data              = df_data["Repuesto"]
        y_garantias         = df_data["Garantia"].to_numpy()
        y_transfer          = df_data["Transferencia"].to_numpy()
        diferencia_gar      = df_data["PorcentajeGarantia"]
        diferencia_transfer = df_data["PorcentajeTransferencia"]

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

        self.plots.bar_indice_consumo(
            fig,
            x_data,
            y_garantias,
            "Garantias",
            diferencia_gar,
            color_garantias,
            custom_garantias
        )

        self.plots.bar_indice_consumo(
            fig,
            x_data,
            y_transfer,
            "Transferencia",
            diferencia_transfer,
            color_transferencias,
            custom_transferencias
        )

        self.default.update_layout(
            fig,
            'Consumo garantias frente a transferencias',
            'Repuesto',
            'Consumo',
            height=665
        )

        self.hover.hover_junto(fig)

        fig.update_layout(
            showlegend=False,
        )

        return fig
