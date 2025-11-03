import random

import numpy as np
import plotly.graph_objects as go

from config.constants import COLORS
from config.enums import IndexTypeEnum
from db_data.crud_services import ServiceRead
from db_data.models.services_model.index_repuesto_model import IndexRepuestoModel
from utils.exception_utils import execute_safely
from utils.streamlit_utils import update_layout, devolver_fecha, top_right_legend


class IndexPlotter:
    def __init__(self, index_type: IndexTypeEnum, tipo_rep: str) -> None:
        self.tipo_rep = tipo_rep
        self.df = ServiceRead().by_rep_and_index(IndexRepuestoModel, self.tipo_rep, index_type)


    @execute_safely
    def create_plot(self) -> tuple[list, str]:
        if self.tipo_rep:
            titulo = f"Indice {self.tipo_rep} ({devolver_fecha(self.df, "UltimaFecha")})"
        else:
            titulo = ""

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
                name="Indice de consumo",

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

            update_layout(fig, repuesto, "Cabecera", "Indice de consumo")
            top_right_legend(fig)

            figuras.append(fig)
        return figuras, titulo
