from typing import Optional
import plotly.graph_objects as go

from src.config.constants import PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH
from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import db_to_df_by_cabecera
from src.db_data.models.services_model.falla_garantias_model import FallaGarantiasModel
from src.utils.streamlit_utils import update_layout


class FallasGarantiasPlotter:
    def __init__(self, cabecera: str) -> None:
        self.cabecera = cabecera
        self.df_data = db_to_df_by_cabecera(FallaGarantiasModel, self.cabecera)


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
                textfont=dict(size=max(300, 300) * 0.2),
                name='Fallos',
                insidetextorientation='horizontal',
                textposition='inside'
            ))

        fig.update_traces(
            hoverinfo='label+value+percent',
            textinfo='value+percent',
        )

        # TODO separar por repuesto el grafico de torta

        if self.cabecera:
            update_layout(fig, f"Fallos garantias {self.cabecera}", '', '', PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH)
        else:
            update_layout(fig, '', '', '', PIE_PLOT_HEIGHT, PIE_PLOT_WIDTH)

        return fig
