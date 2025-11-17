from typing import Union

import plotly.graph_objects as go

from config.constants import PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH, PIE_FONT_SIZE

from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout, top_right_legend
from viewmodels.garantias.falla.datos_vm import DatosGarantiasVM
from viewmodels.garantias.falla.vm import FallaGarantiasVM


class FallasGarantiasPlotter:
    def __init__(self, tipo_repuesto: str, cabecera: str) -> None:
        self.df_data = FallaGarantiasVM().get_df_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)
        self.min_date: str = DatosGarantiasVM().get_min_date()
        self.max_date: str = DatosGarantiasVM().get_max_date()


    @execute_safely
    def create_plot(self) -> Union[go.Figure, None]:
        if not self.df_data.empty and self.min_date is not None and self.max_date is not None:
            labels = self.df_data["Repuesto"]
            values = self.df_data["PromedioTiempoFalla"]
            text = self.df_data["PromedioTiempoFalla"].astype(str)

            fig = go.Figure()

            # TODO: mejorar la leyenda para que sea más clara
            fig.add_trace(go.Pie(
                    labels=labels,
                    values=values,
                    text=text,
                    textfont=dict(size=PIE_FONT_SIZE),
                    name='Fallos',
                    insidetextorientation='horizontal',
                    textposition='auto'
            ))

            fig.update_traces(
                hoverinfo='label+value+percent',
                textinfo='value+percent',
            )

            update_layout(fig, f'Fallos ({self.min_date} - {self.max_date})', '', '', PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH)
            top_right_legend(fig)
            return fig
        return None