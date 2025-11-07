import numpy as np
import pandas as pd

from utils.common_utils import CommonUtils
from utils.exception_utils import execute_safely

from infrastructure.db.crud_services import df_to_db

class DeviationTrend:
    def __init__(self) -> None:
        self.common = CommonUtils()
        

    @execute_safely
    def calculate(self, df) -> None:
        media_cabecera = (round(df.groupby(["Cabecera"])
                            .agg({"IndiceConsumo":"mean"}), 1)
                            .rename(columns={"IndiceConsumo":"MediaCabecera"})
                            .reset_index())
    
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
        media_cabecera["FechaCompleta"] = pd.Timestamp.today().dt.date # type: ignore
        # media_cabecera["FechaCompleta"] = media_cabecera["FechaCompleta"].dt.date

        df_to_db("desviacion_indices", media_cabecera)