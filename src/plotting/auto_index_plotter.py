import random

import pandas as pd
import numpy as np

from typing import Optional
import plotly.graph_objects as go

from src.config.constants import COLORS
from src.services.utils.index_utils import IndexUtils
from src.services.utils.exception_utils import execute_safely
from src.db.crud import sql_to_df_by_type

class AutoIndexPlotter:
    def __init__(self, file: str, directory: str, index_type: str, tipo_rep: str, filtro: Optional[str] = None) -> None:
        self.file = file
        self.index_type = index_type
        self.directory = directory
        self.filtro = filtro
        self.colors = COLORS
        self.tipo_rep = tipo_rep

        # FIXME: funciona pero se ejecuta cada vez que se inicia el programa, arreglar
        IndexUtils().prepare_data(self.index_type, self.file, self.directory, self.tipo_rep, self.filtro) # cargo los datos
        self.df = sql_to_df_by_type("indice_repuesto", self.tipo_rep)
            

    def create_plot(self) -> list:
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
                marker=dict(color=self.colors[random.randint(0,19)])
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
                yaxis_title='Consumo',
                xaxis_title='Cabecera',
                showlegend=True
            )

            figuras.append(fig)
        return figuras


    @execute_safely
    def devolver_fecha(self) -> str:
        return pd.to_datetime(self.df["UltimaFecha"].unique()).strftime("%d-%m-%Y")[0]
