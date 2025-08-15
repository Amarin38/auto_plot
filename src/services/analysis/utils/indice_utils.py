import pandas as pd

from numpy import ndarray
from typing import List


class IndiceUtils:
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
