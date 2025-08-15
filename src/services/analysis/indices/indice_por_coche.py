import pandas as pd

from typing import List, Dict, Union, Any

from src.config import MAIN_PATH
from src.services import IndiceUtils

class IndicePorCoche:
    def __init__(self, file_consumo: str) -> None:
        self.file_consumo = file_consumo

        self.df_coches = pd.read_excel(f"{MAIN_PATH}/src/data/excel_data/coches_por_cabecera.xlsx", engine="calamine")
        self.df_consumo = pd.read_excel(f"{MAIN_PATH}/out/{self.file_consumo}-S.xlsx", engine="calamine")


    def calcular(self) -> List[Union[pd.DataFrame, str]]:
        lista_indices: List[Dict[str, Union[Any, float]]] = []

        repuestos = self.df_consumo["Repuesto"].unique() 
        cabeceras = self.df_consumo["Cabecera"].unique()

        for cab in cabeceras:
            cant_coches = self.df_coches.loc[self.df_coches["Cabecera"] == cab, 
                                             "CantidadCoches"].iloc[0] # type: ignore
            
            for rep in repuestos:
                total_consumo_por_cabecera = self.df_consumo.loc[(self.df_consumo["Repuesto"] == rep) & 
                                                                 (self.df_consumo["Cabecera"] == cab),
                                                                 ['Cantidad']].sum()
                
                total_coste_por_cabecera = self.df_consumo.loc[(self.df_consumo["Repuesto"] == rep) &
                                                               (self.df_consumo["Cabecera"] == cab), 
                                                               ['Precio']].sum()

                indice_consumo: pd.Series[float] = (total_consumo_por_cabecera*100)/cant_coches
                lista_indices.append({
                    "Cabecera":cab,
                    "Repuesto":rep,
                    "TotalConsumo":total_consumo_por_cabecera.iloc[0],
                    "TotalCoste":total_coste_por_cabecera.iloc[0],
                    "IndiceConsumo":round(indice_consumo.iloc[0], 1)
                })

        df_indice: pd.DataFrame = pd.DataFrame(lista_indices)
        df_indice.to_excel(f"{MAIN_PATH}/out/indice_por_coche.xlsx")
        return [df_indice, IndiceUtils()._fecha_titulo(self.df_consumo)]
