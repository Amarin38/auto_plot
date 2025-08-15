import json

import pandas as pd

from numpy import ndarray
from typing import Dict, List, Union, Any

from src.config.constants import MAIN_PATH

class IndicePorCoche:
    def __init__(self, file_consumo: str) -> None:
        self.file_consumo = file_consumo

        self.df_coches = pd.read_excel(f"{MAIN_PATH}/excel_info/coches_por_cabecera.xlsx", engine="calamine")
        self.df_consumo = pd.read_excel(f"{MAIN_PATH}/out/{self.file_consumo}-S.xlsx", engine="calamine")


    def calcular(self) -> List[Union[pd.DataFrame, str]]:
        lista_indices: List[Dict[str, Union[Any, float]]] = []

        repuestos: ndarray = self.df_consumo["Repuesto"].unique() 
        cabeceras: ndarray = self.df_consumo["Cabecera"].unique()

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
        return [df_indice, _IndiceUtils()._fecha_titulo(self.df_consumo)]


class IndicePorMotor:
    def __init__(self, file_consumo: str) -> None:
        self.file_consumo = file_consumo

        self.df_motores = pd.read_excel(f"{MAIN_PATH}/excel_info/motores_por_cabecera.xlsx", engine="calamine")
        self.df_consumo = pd.read_excel(f"{MAIN_PATH}/out/{self.file_consumo}-S.xlsx", engine="calamine")


    def calcular(self) -> List[Union[pd.DataFrame, str]]:
        indices: List[str] = []

        cabeceras: ndarray = self.df_motores["Cabecera"].unique()
        repuestos: ndarray = self.df_motores["Repuesto"].unique()

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
        return [df_indice, _IndiceUtils()._fecha_titulo(self.df_consumo)]


class IndiceGomeria:
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
        meses: pd.Index = _IndiceUtils()._generar_lista_meses(self.meses_diferencia)
        indice_consumo_por_mes: Dict[str, float] = {}

        with open(f"{MAIN_PATH}/json/cubiertas_armadas.json", "r") as f1:
            data_armadas = json.load(f1)
        
        for m in meses:
            total_consumo = round(self.data_consumo["plata"][0][m]/data_armadas["cantidad"][0][m], 2) 
            indice_consumo_por_mes.update({m:total_consumo})
        
        return indice_consumo_por_mes


class _IndiceUtils:
    @staticmethod
    def _media_consumo(indice_consumo: List[int], con_cero: bool) -> float:
        total_consumo = sum(indice_consumo)
        cantidad_indices = 0

        if con_cero:
            cantidad_indices = len(indice_consumo)
        else:
            for indice in indice_consumo:
                if indice != 0:
                    cantidad_indices += 1
            

        if cantidad_indices != 0:
            return round(total_consumo/cantidad_indices,2)
        else:
            return 0

    @staticmethod
    def _fecha_titulo(df: pd.DataFrame) -> str:
        """
        Devuelve la fecha del titulo basandose en el archivo introducido.
        """
        df["FechaCompleta"] = pd.to_datetime(df["FechaCompleta"], errors="coerce")
        fechas: ndarray = df["FechaCompleta"].unique()
        fechas_min = fechas.min().strftime("%Y-%m")
        fechas_max = fechas.max().strftime("%Y-%m")

        return f"{fechas_min} a {fechas_max}"
    
    @staticmethod
    def _generar_lista_meses(meses_diferencia) -> pd.Index:
        hoy = pd.Timestamp.today()
        diferencia = pd.date_range(hoy - pd.Timedelta(days=30*meses_diferencia))

        return pd.DatetimeIndex(diferencia.strftime("%Y-%B").unique())
