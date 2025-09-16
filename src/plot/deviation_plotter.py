import pandas as pd

from typing import Optional

import plotly.graph_objects as go

from src.config.constants import COLORS

from src.services.analysis.deviation_trend import DeviationTrend
from src.utils.exception_utils import execute_safely

from src.db.crud_services import db_to_df


class DeviationPlotter:
    def __init__(self, df: Optional[pd.DataFrame] = None) -> None:
        if df is not None:
            DeviationTrend().calcular_desviaciones_totales(df)

        self.df = db_to_df("deviation")
            
    @execute_safely
    def create_plot(self) -> go.Figure:
        x_data = self.df["Cabecera"] 
        y_data = self.df["Desviacion"] 
        median = self.df["MediaDeMedias"]

        fecha = pd.to_datetime(self.df["FechaCompleta"].unique()).strftime("%d-%m-%Y")
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
            
        
        fig.update_layout(
            title=f"Desviacion {fecha[0]}",
            width=200,
            height=600,

            xaxis=dict(
                title='Cabecera',
                showticklabels=True
            ),

            yaxis=dict(
                title='Desviacion en %',
                showticklabels=True
            ),
            
            showlegend=True
        )

        return fig

