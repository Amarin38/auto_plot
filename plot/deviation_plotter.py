import pandas as pd
import plotly.graph_objects as go

from config.constants import COLORS, FILE_STRFTIME_DMY
from db_data.crud_services import ServiceRead
from db_data.models.services_model.deviation_model import DeviationModel
from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout, top_right_legend


class DeviationPlotter:
    def __init__(self) -> None:
        self.df = ServiceRead().all_df(DeviationModel)

    @execute_safely
    def create_plot(self) -> go.Figure:
        x_data = self.df["Cabecera"] 
        y_data = self.df["Desviacion"]

        y_porcentual = self.df["Desviacion"].astype(str) + "%"

        fecha = pd.to_datetime(self.df["FechaCompleta"].unique()).strftime(FILE_STRFTIME_DMY)
        color = COLORS[9]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            name="Desviaciones",
            
            text=y_porcentual,
            textposition="outside",
            textfont=dict(
                size=11,
                color='white', 
                family='Arial'  
            ),

            marker=dict(color=color)
        ))


        fig.add_trace(go.Scatter(
            x=x_data,
            y=[0] * len(x_data),
            mode='lines',

            name="Centro de desviaciones (Media)",
            line=dict(color='red', dash='dash')
        ))


        for cab in x_data:
            fig.add_shape(type="line",
                x0=cab, y0=-105, x1=cab, y1=105,
                line=dict(color=color, width=1))
            
        update_layout(fig, f"Desviacion {fecha[0]}", 'Cabecera', 'Desviacion de la media en %', 600, 200)
        top_right_legend(fig)

        fig.update_layout(

        )
        return fig