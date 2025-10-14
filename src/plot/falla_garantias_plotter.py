import plotly.graph_objects as go

from src.config.constants import PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH, PIE_FONT_SIZE
from src.db_data.crud_services import db_to_df_by_cabecera_and_repuesto
from src.db_data.models.services_model.falla_garantias_model import FallaGarantiasModel
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import update_layout, top_right_legend


class FallasGarantiasPlotter:
    def __init__(self, cabecera: str, tipo_repuesto: str) -> None:
        self.cabecera = cabecera
        self.tipo_repuesto = tipo_repuesto
        self.df_data = db_to_df_by_cabecera_and_repuesto(FallaGarantiasModel, self.cabecera, self.tipo_repuesto)


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

        update_layout(fig, '', '', '', PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH)
        top_right_legend(fig)
        return fig
