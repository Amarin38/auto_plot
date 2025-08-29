import numpy as np

from config.constants import OUT_PATH
from services.utils.common_utils import CommonUtils
from services.utils.exception_utils import execute_safely

class DeviationTrend:
    @staticmethod
    @execute_safely
    def calcular_desviacion(valor_indice, valor_media) -> float:
        if valor_media == 0:
            return 0
        return round(((valor_indice - valor_media) / valor_media) * 100, 0)


    @staticmethod
    @execute_safely
    def calcular_desviaciones_totales() -> None:
        df = CommonUtils()._append_df("todos_indices", "todos indices", True)

        media_cabecera = round(df.groupby(["Cabecera"]).agg({"IndiceConsumo":"mean"}), 1).rename(columns={"IndiceConsumo":"MediaCabecera"}).reset_index()#type:ignore
       
        media_cabecera["MediaDeMedias"] = round(media_cabecera["MediaCabecera"].mean(), 2)
        media_cabecera["Diferencia"] = round(media_cabecera["MediaCabecera"] - media_cabecera["MediaDeMedias"], 2)
        media_cabecera["Desviacion"] = round((media_cabecera["Diferencia"] / media_cabecera["MediaDeMedias"])*100, 2)
        
        conditions = [
            (media_cabecera["Desviacion"] > 0) & (media_cabecera["Desviacion"] <= 50),
            (media_cabecera["Desviacion"] > 50),
            (media_cabecera["Desviacion"] == 0),
            (media_cabecera["Desviacion"] < 0) & (media_cabecera["Desviacion"] >= -50),
            (media_cabecera["Desviacion"] < -50)
        ]
        choices = ("Encima","Muy por encima", "Igual", "Debajo", "Muy por debajo")
        media_cabecera["DesviacionPor"] = np.select(conditions, choices, default="Debajo")
        media_cabecera.to_excel(f"{OUT_PATH}/Desviacion_por_cabecera.xlsx")
        print(media_cabecera)
    