from typing import Union

import pandas as pd
import plotly.graph_objects as go

from config.constants_views import PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH, PIE_FONT_SIZE
from config.enums_colors import FallaGarantiasColorsEnum

from utils.exception_utils import execute_safely
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents


class FallaGarantiasPlotter:
    def __init__(self, df: pd.DataFrame, min_date: str, max_date: str) -> None:
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.df_data = df
        self.min_date = min_date
        self.max_date = max_date


    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        labels = self.df_data["Repuesto"]
        values = self.df_data["PromedioTiempoFalla"].to_numpy()
        text = self.df_data["PromedioTiempoFalla"].astype(str)

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

        self.default.update_layout(fig, f'Fallos ({self.min_date} - {self.max_date})',
                                   '', '', PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH)
        self.hover.hover_x(fig)

        return fig
