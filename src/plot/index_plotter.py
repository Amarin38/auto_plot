import random

import pandas as pd
import numpy as np
import plotly.graph_objects as go

from typing import Optional, Literal

from src.config.constants import COLORS, FILE_STRFTIME
from src.config.enums import IndexTypeEnum

from src.utils.exception_utils import execute_safely

from src.db_data.crud_services import db_to_df_by_repuesto_and_index_type
from src.db_data.models.services_model.index_repuesto_model import IndexRepuestoModel

class IndexPlotter:
    @execute_safely
    def create_plot(self, index_type: IndexTypeEnum, tipo_rep: str, filtro: Optional[str] = None) -> list:
        self.df = db_to_df_by_repuesto_and_index_type(IndexRepuestoModel, tipo_rep, index_type)

        todos_repuestos = self.df["Repuesto"].unique()
        figuras = []

        for repuesto in todos_repuestos:
            df_repuesto = self.df.loc[self.df["Repuesto"] == repuesto]

            x_data = df_repuesto["Cabecera"] 
            y_data = df_repuesto["IndiceConsumo"] 
            median = [round(y_data.replace(0, np.nan).mean(), 1)] * len(x_data)

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=x_data,
                y=y_data,
                name="Consumo",

                text=y_data,
                textposition="auto",
                textfont=dict(
                    size=11,
                    color='white', 
                    family='Arial'  
                ),
                
                marker=dict(color=COLORS[random.randint(0,19)])
            ))


            fig.add_trace(go.Scatter(
                x=x_data,
                y=median,
                mode="lines",
                name=f"Media ({median[0]})",
                line=dict(color='red', dash='dash')
            ))


            fig.update_layout(
                title=f"{repuesto}",

                xaxis=dict(
                    title='Cabecera',
                    showticklabels=True
                ),
                
                yaxis=dict(
                    title='Consumo',
                    showticklabels=True
                ),

                showlegend=True
            )

            figuras.append(fig)
        return figuras


    @execute_safely
    def _devolver_fecha(self) -> str:
        return pd.to_datetime(self.df["UltimaFecha"].unique()).strftime(FILE_STRFTIME)[0]
    
    @execute_safely
    def devolver_titulo(self, rep: str) -> str:
        return f"Indice {rep} ({self._devolver_fecha()})"
