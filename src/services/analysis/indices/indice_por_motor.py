import pandas as pd
import numpy as np

from typing import List, Union

from config.constants import MAIN_PATH
from services.analysis.indices.utils.indice_utils import IndiceUtils
from services.data_cleaning.listado_existencias import ArreglarListadoExistencias


class IndicePorMotor:
    def __init__(self, file_consumo: str, dir_files: str) -> None:
        self.file_consumo = file_consumo
        self.dir_files = dir_files

        self.listado = ArreglarListadoExistencias(self.file_consumo, self.dir_files).arreglar_listado()

        self.df_motores = pd.read_excel(f"{MAIN_PATH}/src/data/excel_data/motores_por_cabecera.xlsx", engine="calamine")
        self.df_consumo = pd.read_excel(f"{MAIN_PATH}/out/{self.file_consumo}-S.xlsx", engine="calamine")


    def calcular(self) -> List[Union[pd.DataFrame, str]]:
        agrupado = self.df_consumo.groupby(['Cabecera', 'Repuesto']).agg({ # agrupo por columna
            'Cantidad':'sum', # le digo que quiero hacer en cada columna agrupada
        }).reset_index()

        df_con_motor = agrupado.merge(self.df_motores, on=["Cabecera", "Repuesto"], how="right") # hago join con la cantidad de coches para hacer el cálculo
        df_con_motor["IndiceConsumo"] = round((df_con_motor["Cantidad"]*100) / df_con_motor["CantidadMotores"], 1) # hago el cálculo y se lo asigno a una nueva columna

        df_indice = df_con_motor[['Cabecera', 'Repuesto', 'IndiceConsumo']]
        df_indice["IndiceConsumo"].replace([np.inf, -np.inf], np.nan, inplace=True)
        df_indice.dropna(subset=["IndiceConsumo"], inplace=True)
        
        df_indice.to_excel(f"{MAIN_PATH}/out/{self.file_consumo}_indice_por_motor.xlsx")
        return [df_indice, IndiceUtils()._fecha_titulo(self.df_consumo)]


