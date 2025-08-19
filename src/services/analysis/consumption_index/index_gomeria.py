import json

import pandas as pd

from typing import Dict

from config.constants import MAIN_PATH
from src.services.analysis.consumption_index.utils.index_utils import IndexUtils

class IndexGomeria:
    def __init__(self, file: str, diff_months: int) -> None:
        self.file = file
        self.diff_months = diff_months


    def calculate_trend(self) -> None:
        df = pd.read_excel(f"{self.file}.xlsx", engine="calamine")
        with open("src/data/json_data/meses.json", "r") as m:
            meses: Dict[str,int] = json.load(m)

        consumo_cantidad: Dict[str, int] = {}
        consumo_coste: Dict[str, float] = {}
        
        for mes, num_mes in meses.items():
            df_filtrado = df[df["FechaCompleta"].dt.month == num_mes] # separo por mes

            cantidad_total_por_mes = df.iloc[df_filtrado.index, 11].sum() # sumo consumo en ese mes
            precio_total_por_mes = (df.iloc[df_filtrado.index, 11] * df.iloc[df_filtrado.index, 13]).sum() # sumo el consumo en plata en ese mes 

            consumo_cantidad.update({
                mes:int(cantidad_total_por_mes)
                })
            consumo_coste.update({
                mes:round(float(precio_total_por_mes),2)
                })
        
        df_final: pd.DataFrame = pd.DataFrame({
                                            "Cantidad":[consumo_cantidad],
                                            "Coste":[consumo_coste]
                                              })
        
        df_final.to_excel(f"{MAIN_PATH}/src/data/excel_data/cubiertas_consumo_{self.file}.xlsx")


    def update_tire_values(self) -> Dict[str, float]:
        meses: pd.Index = IndexUtils()._create_months_list(self.diff_months)
        indice_consumo_por_mes: Dict[str, float] = {}

        data_consumo = pd.read_excel(f"{MAIN_PATH}/src/data/excel_data/cubiertas_consumo_{self.file}.xlsx", engine="calamine")
        with open(f"{MAIN_PATH}/src/data/json_data/cubiertas_armadas.json", "r") as f1:
            data_armadas = json.load(f1)
        
        for m in meses:
            total_consumo = round(data_consumo["plata"][0][m]/data_armadas["cantidad"][0][m], 2) 
            indice_consumo_por_mes.update({m:total_consumo})
        
        return indice_consumo_por_mes
