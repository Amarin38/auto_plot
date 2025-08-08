import pandas as pd

from pathlib import Path
from numpy import ndarray
from typing import Dict, List, Union, Any

# TODO agregar mas abstraccion de clases, sacar fecha_titulo y media_consumo

class IndiceConsumo:
    def __init__(self, file_consumo: str) -> None:
        self._main_path = Path.cwd()
        self.file_consumo = file_consumo
        self.df_motores = pd.read_excel(f"{self._main_path}/excel_info/motores_por_cabecera.xlsx", engine="calamine")
        self.df_coches = pd.read_excel(f"{self._main_path}/excel_info/coches_por_cabecera.xlsx", engine="calamine")
        self.df_consumo = pd.read_excel(f"{self._main_path}/excel/{self.file_consumo}-S.xlsx", engine="calamine")
        

    def calcular_indice_por_coche(self) -> List[Union[pd.DataFrame, str]]:
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
        df_indice.to_excel(f"{self._main_path}/excel/indice_por_coche.xlsx")
        return [df_indice, self.fecha_titulo(self.df_consumo)]


    def calcular_indice_por_motores(self) -> List[Union[pd.DataFrame, str]]:
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
        df_indice.to_excel(f"{self._main_path}/excel/indice_por_motor.xlsx")
        return [df_indice, self.fecha_titulo(self.df_consumo)]


    def media_consumo(self, indice_consumo: List[int], con_cero: bool) -> float:
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


    def fecha_titulo(self, df: pd.DataFrame) -> str:
        """
        Devuelve la fecha del titulo basandose en el archivo introducido.
        """
        df["FechaCompleta"] = pd.to_datetime(df["FechaCompleta"], errors="coerce")
        fechas: ndarray = df["FechaCompleta"].unique()
        fechas_min = fechas.min().strftime("%Y-%m")
        fechas_max = fechas.max().strftime("%Y-%m")

        return f"{fechas_min} a {fechas_max}"


class IndicePorCoche:
    pass

class IndicePorMotor:
    pass