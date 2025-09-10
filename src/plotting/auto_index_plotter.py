import random

import pandas as pd
import numpy as np
import plotly.graph_objects as go

from typing import Optional, Literal

from src.config.constants import COLORS
from src.config.constants import MAIN_PATH
from src.config.enums import IndexTypeEnum

from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.analysis.consumption_index.index_by_motor import IndexByMotor
from src.services.analysis.consumption_index.index_by_vehicle import IndexByVehicle 
from src.services.utils.exception_utils import execute_safely
from src.services.utils.common_utils import CommonUtils

from src.db.crud import sql_to_df_by_type
from src.db.indice_repuesto_model import IndiceRepuesto

class AutoIndexPlotter:
    def __init__(self, directory: str, index_type: Literal["MOTOR", "VEHICLE"], tipo_rep: str, filtro: Optional[str] = None) -> None:
        self.index_type = index_type
        self.directory = directory
        self.filtro = filtro
        self.colors = COLORS
        self.tipo_rep = tipo_rep

        dir_exists = CommonUtils.check_file_exists(MAIN_PATH, directory)
        if dir_exists:
            self.prepare_data()

        self.df = sql_to_df_by_type(IndiceRepuesto, self.tipo_rep)
            

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
    def prepare_data(self) -> None:
        df = InventoryDataCleaner().run_all(self.directory)

        # if index_type == IndexTypeEnum.BY_MOTOR.value:
            # df_updated = InventoryUpdate().rows_by_dict(df, file, "motores") #FIXME: le paso un file normal pero del otro lado es un json
            # df_updated.to_excel(f"{OUT_PATH}/{file}-S.xlsx")
            
            # IndexByMotor(file, directory, tipo_repuesto).calculate_index()
        
        
        if self.index_type == IndexTypeEnum.BY_VEHICLE.value:
            IndexByVehicle(self.directory, self.tipo_rep, self.filtro).calculate_index(df)
        else:
            raise ValueError(f"Tipo de indice no soportado: {self.index_type}")


    @execute_safely
    def devolver_fecha(self) -> str:
        return pd.to_datetime(self.df["UltimaFecha"].unique()).strftime("%d-%m-%Y")[0]
    
    @execute_safely
    def devolver_titulo(self, rep) -> str:
        return f"Indice {rep} ({self.devolver_fecha()})"
