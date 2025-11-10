from datetime import datetime as dt

import plotly.graph_objects as go

from config.constants import PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH, PIE_FONT_SIZE, PAGE_STRFTIME_YMD

from infrastructure.repositories.common.crud_common import CommonRead
from infrastructure.repositories.services.crud_services import ServiceRead

from infrastructure.db.models.services.falla_garantias_model import FallaGarantiasModel
from infrastructure.db.models.common.datos_garantias_model import DatosGarantiasModel

from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout, top_right_legend
from viewmodels.falla_garantias_vm import FallaGarantiasVM


class FallasGarantiasPlotter:
    def __init__(self, tipo_repuesto: str, cabecera: str) -> None:
        read = CommonRead()
        self.df_data = FallaGarantiasVM().get_df_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)
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
