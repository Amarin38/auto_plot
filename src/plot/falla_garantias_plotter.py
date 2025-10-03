import plotly.graph_objects as go

from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import db_to_df_by_cabecera
from src.db_data.models.services_model.falla_garantias_model import FallaGarantiasModel


class FallasGarantiasPlotter:
    @execute_safely
    def create_plot(self, cabecera: str):
        df_data = db_to_df_by_cabecera(FallaGarantiasModel, cabecera)

        labels = df_data["Repuesto"]
        values = df_data["PromedioTiempoFalla"]
        text = df_data["PromedioTiempoFalla"].astype(str)

        fig = go.Figure(
                data=[go.Pie(
                        labels=labels,
                        values=values,
                        text=text,
                        textfont=dict(size=18),
                        name='Fallos',
                        insidetextorientation='radial',
                        textposition='inside'
                    )
                ]
        )

        fig.update_traces(
            hoverinfo='label+value+percent',
            textinfo='label+percent',
        )

        fig.update_layout(
            title=f'{cabecera} Falla Garantias',
            showlegend=True,
        )

        return fig
    
