import json

import pandas as pd

from typing import Dict

from src.config.constants import MAIN_PATH


class ConsumoGomeria:
    def __init__(self, archivo: str, meses_diferencia: int) -> None:
        self.archivo = archivo
        self.meses_diferencia = meses_diferencia
        self.df = pd.read_excel(f"{self.archivo}.xlsx", engine="calamine")
        self.data_consumo = pd.read_excel(f"{MAIN_PATH}/excel_info/cubiertas_consumo_{self.archivo}.xlsx", engine="calamine")


    def calcular_consumo_por_mes_gomeria(self) -> None:
        with open("json/meses.json", "r") as m:
            meses: Dict[str,int] = json.load(m)

        consumo_cantidad: Dict[str, int] = {}
        consumo_coste: Dict[str, float] = {}
        
        for mes, num_mes in meses.items():
            df_filtrado = self.df[self.df["FechaCompleta"].dt.month == num_mes] # separo por mes

            cantidad_total_por_mes = self.df.iloc[df_filtrado.index, 11].sum() # sumo consumo en ese mes
            precio_total_por_mes = (self.df.iloc[df_filtrado.index, 11] * self.df.iloc[df_filtrado.index, 13]).sum() # sumo el consumo en plata en ese mes 

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
        
        df_final.to_excel(f"{MAIN_PATH}/excel_info/cubiertas_consumo_{self.archivo}.xlsx")


    def actualizar_valores_cubiertas(self) -> Dict[str, float]:
        meses: pd.Index = self._generar_lista_meses()
        indice_consumo_por_mes: Dict[str, float] = {}

        with open(f"{MAIN_PATH}/json/cubiertas_armadas.json", "r") as f1:
            data_armadas = json.load(f1)
        
        for m in meses:
            total_consumo = round(self.data_consumo["plata"][0][m]/data_armadas["cantidad"][0][m], 2) 
            indice_consumo_por_mes.update({m:total_consumo})
        
        return indice_consumo_por_mes


    def _generar_lista_meses(self) -> pd.Index:
        hoy = pd.Timestamp.today()
        diferencia = pd.date_range(hoy - pd.Timedelta(days=30*self.meses_diferencia))

        return pd.DatetimeIndex(diferencia.strftime("%Y-%B").unique())
