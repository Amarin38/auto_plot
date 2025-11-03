from datetime import datetime as dt

import plotly.graph_objects as go

from config.constants import PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH, PIE_FONT_SIZE, PAGE_STRFTIME_YMD
from db_data.crud_common import CommonRead
from db_data.crud_services import ServiceRead
from db_data.models.services_model.falla_garantias_model import FallaGarantiasModel
from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout, top_right_legend

from db_data.models.common_model.datos_garantias_model import DatosGarantiasModel

class FallasGarantiasPlotter:
    def __init__(self, cabecera: str, tipo_repuesto: str) -> None:
        read = CommonRead()
        self.df_data = ServiceRead.by_rep_and_cabecera(FallaGarantiasModel, cabecera, tipo_repuesto)
        self.min_date: dt = read.min_date(DatosGarantiasModel).strftime(PAGE_STRFTIME_YMD)
        self.max_date: dt = read.max_date(DatosGarantiasModel).strftime(PAGE_STRFTIME_YMD)

    @execute_safely
    def create_plot(self):
        labels = self.df_data["Repuesto"]
        values = self.df_data["PromedioTiempoFalla"]
        text = self.df_data["PromedioTiempoFalla"].astype(str)

        fig = go.Figure()

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
