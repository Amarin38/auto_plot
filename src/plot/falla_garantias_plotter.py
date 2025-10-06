import plotly.graph_objects as go

from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import db_to_df_by_cabecera
from src.db_data.models.services_model.falla_garantias_model import FallaGarantiasModel


class FallasGarantiasPlotter:
    @execute_safely
    def create_plot(self, cabecera: str):
        self.df_data = db_to_df_by_cabecera(FallaGarantiasModel, cabecera)

        labels = self.df_data["Repuesto"]
        values = self.df_data["PromedioTiempoFalla"]
        text = self.df_data["PromedioTiempoFalla"].astype(str)

        fig = go.Figure(
                data=[go.Pie(
                        labels=labels,
                        values=values,
                        text=text,
                        textfont=dict(size=max(300, 300) * 0.2),
                        name='Fallos',
                        insidetextorientation='horizontal',
                        textposition='inside'
                    )
                ]
        )

        fig.update_traces(
            hoverinfo='label+value+percent',
            textinfo='value+percent',
        )

        # TODO separar por repuesto el grafico de torta
        fig.update_layout(
            # title=f'{cabecera} Falla Garantias',
            legend=dict(
                title='Repuesto',
                orientation='v',
                yanchor='top',
                y=1.02,
                xanchor='right',
                x=1,
                font=dict(size=13)
            ),
            showlegend=True,

            height=700,
            width=700,
        )

        return fig
    
    @execute_safely
    def devolver_titulo(self, cabecera: str) -> str:
        if self.df_data.size == 0:
            return ""
        return f"Fallos garantias {cabecera}"