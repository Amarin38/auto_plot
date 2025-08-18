import pandas as pd

from typing import List, Union

from src.config import MAIN_PATH
from src.services.analysis.indices.utils.indice_utils import IndiceUtils


class IndicePorMotor:
    def __init__(self, file_consumo: str) -> None:
        self.file_consumo = file_consumo

        self.df_motores = pd.read_excel(f"{MAIN_PATH}/src/data/excel_data/motores_por_cabecera.xlsx", engine="calamine")
        self.df_consumo = pd.read_excel(f"{MAIN_PATH}/out/{self.file_consumo}-S.xlsx", engine="calamine")


    def calcular(self) -> List[Union[pd.DataFrame, str]]:
        indices: List[str] = []

        cabeceras = self.df_motores["Cabecera"].unique()
        repuestos = self.df_motores["Repuesto"].unique()

        for cab in cabeceras:
            cab_consumo: pd.Series[bool] = self.df_consumo["Cabecera"] == cab 
            cab_motores: pd.Series[bool] = self.df_motores["Cabecera"] == cab 

            for rep in repuestos:
                indice_consumo: float = 0

                rep_consumo: pd.Series[bool] = self.df_consumo["Repuesto"] == rep
                rep_motores: pd.Series[bool] = self.df_motores["Repuesto"] == rep

                cantidad_consumo = df_consumo.loc[cab_consumo & rep_consumo, "Cantidad"].sum() # type: ignore
                cantidad_motores = df_motores.loc[cab_motores & rep_motores, "Cantidad"].iloc[0] # type: ignore
                
                if cantidad_motores != 0:
                    indice_consumo = (cantidad_consumo*100)/cantidad_motores

                indices.append({
                    "Cabecera":cab,
                    "Repuesto":rep,
                    "IndiceConsumo":float(round(indice_consumo, 1))    
                }) # type: ignore
        
        df_indice: pd.DataFrame = pd.DataFrame(indices)
        df_indice.to_excel(f"{MAIN_PATH}/out/indice_por_motor.xlsx")
        return [df_indice, IndiceUtils()._fecha_titulo(self.df_consumo)]


