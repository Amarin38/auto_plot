from typing import Union

from config.enums_colors import CustomMetricColorsEnum
from config.constants_views import PIE_FONT_SIZE, PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH
import plotly.graph_objects as go

from utils.exception_utils import execute_safely
from viewmodels.conteo_stock.vm import ConteoStockVM
from viewmodels.plotly_components import HoverComponents, DefaultUpdateLayoutComponents


class ConteoStockPlotter:
    def __init__(self) -> None:
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.df = ConteoStockVM().get_df()


    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df.empty:
            df_grouped = self.df["Resultado"].value_counts().reset_index()
            df_grouped.columns = ["Resultado", "Cantidad"]


            fig = go.Figure()

            fig.add_trace(go.Pie(
                    labels=df_grouped["Resultado"],
                    values=df_grouped["Cantidad"],
                    text=df_grouped["Resultado"],
                    textfont=dict(
                        size=PIE_FONT_SIZE
                    ),
                    name='Conteo',
                    insidetextorientation='horizontal',
                    textposition='auto',
                    customdata=CustomMetricColorsEnum.as_list(),
                    marker=dict(colors=CustomMetricColorsEnum.as_list()),
                    hovertemplate="""
<b>
<span style='color:%{customdata}'>%{label}</span><br>
%{value} (<span style='color:%{customdata}'>%{percent}</span>)
</b>
<extra></extra>
""",
            ))

            self.default.update_layout(fig, "",'', '', PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH)
            self.hover.hover_x(fig)

            fig.update_traces(
                textinfo='label+percent',
                textfont=dict(size=20),
                showlegend=False,
            )

            fig.update_traces(
                hoverlabel=dict(
                    align="left"
                )
            )
            return fig
        return None
