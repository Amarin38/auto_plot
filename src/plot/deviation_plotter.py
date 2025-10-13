import pandas as pd
import plotly.graph_objects as go

from src.config.constants import COLORS, FILE_STRFTIME_DMY
from src.db_data.crud_services import db_to_df
from src.db_data.models.services_model.deviation_model import DeviationModel
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import update_layout


class DeviationPlotter:
    def __init__(self) -> None:
        self.df = db_to_df(DeviationModel)

    @execute_safely
    def create_plot(self) -> go.Figure:
        x_data = self.df["Cabecera"] 
        y_data = self.df["Desviacion"] 
        median = self.df["MediaDeMedias"]

        fecha = pd.to_datetime(self.df["FechaCompleta"].unique()).strftime(FILE_STRFTIME_DMY)
        color = COLORS[9]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            name="Desviaciones",
            
            text=y_data,
            textposition="auto",
            textfont=dict(
                size=11,
                color='white', 
                family='Arial'  
            ),

            marker=dict(color=color)
        ))


        fig.add_trace(go.Scatter(
            x=x_data,
            y=median,
            mode='lines',

            name=f"Media desviaciones({median[0]})",
            line=dict(color='red', dash='dash')
        ))

        for cab in x_data:
            fig.add_shape(type="line",
                x0=cab, y0=-105, x1=cab, y1=105,
                line=dict(color=color, width=1))
            
        update_layout(fig, f"Desviacion {fecha[0]}", 'Cabecera', 'Desviacion en %', 600, 200)

        fig.update_layout(
            legend=dict(
                orientation='v',
                yanchor='top',
                y=1.15,
                xanchor='right',
                x=1,
                font=dict(size=13)
            ),
        )

        return fig