import numpy as np

from src.config.constants import OUT_PATH
from src.utils.common_utils import CommonUtils
from src.utils.exception_utils import execute_safely

class DeviationTrend:
    @staticmethod
    @execute_safely
    def calcular_desviaciones_totales() -> None:
        df = CommonUtils().append_df("todos indices")

        media_cabecera = round(df.groupby(["Cabecera"]).agg({"IndiceConsumo":"mean"}), 1).rename(columns={"IndiceConsumo":"MediaCabecera"}).reset_index() # type:ignore
       
        media_cabecera["MediaDeMedias"] = round(media_cabecera["MediaCabecera"].mean(), 2)
        media_cabecera["Diferencia"] = round(media_cabecera["MediaCabecera"] - media_cabecera["MediaDeMedias"], 2)
        media_cabecera["Desviacion"] = round((media_cabecera["Diferencia"] / media_cabecera["MediaDeMedias"]) * 100, 2)
        
        conditions = [
            (media_cabecera["Desviacion"] > 0) & (media_cabecera["Desviacion"] <= 50),
            (media_cabecera["Desviacion"] > 50),
            (media_cabecera["Desviacion"] == 0),
            (media_cabecera["Desviacion"] < 0) & (media_cabecera["Desviacion"] >= -50),
            (media_cabecera["Desviacion"] < -50)
        ]
        choices = ("Encima", "Muy por encima", "Igual", "Debajo", "Muy por debajo")
        media_cabecera["DesviacionPor"] = np.select(conditions, choices, default="Debajo")
        media_cabecera.to_excel(f"{OUT_PATH}/Desviacion_por_cabecera.xlsx")
    