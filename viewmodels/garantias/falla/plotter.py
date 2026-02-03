from typing import Union

import plotly.graph_objects as go

from config.constants_views import PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH, PIE_FONT_SIZE
from config.enums_colors import FallaGarantiasColorsEnum

from utils.exception_utils import execute_safely
from viewmodels.plotly_components import DefaultUpdateLayoutComponents, HoverComponents
from viewmodels.garantias.falla.datos_vm import DatosGarantiasVM
from viewmodels.garantias.falla.vm import FallaGarantiasVM


class FallaGarantiasPlotter:
    def __init__(self, tipo_repuesto: str, cabecera: str) -> None:
        self.default = DefaultUpdateLayoutComponents()
        self.hover = HoverComponents()
        self.df_data = FallaGarantiasVM().get_df_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)
        self.min_date: str = DatosGarantiasVM().get_min_date()
        self.max_date: str = DatosGarantiasVM().get_max_date()


    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df_data.empty and self.min_date and self.max_date:
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
        return None