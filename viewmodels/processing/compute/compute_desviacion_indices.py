from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy.dialects.mssql.information_schema import columns

from config.constants_common import TODAY_DATE_FILE_YMD, FILE_STRFTIME_YMD
from utils.common_utils import CommonUtils
from utils.exception_utils import execute_safely
from viewmodels.consumo.indice.desviacion.vm import DesviacionIndicesVM
from viewmodels.consumo.indice.vm import IndiceConsumoVM


class DeviationTrend:
    def __init__(self) -> None:
        self.common = CommonUtils()
        self.indices = IndiceConsumoVM()
        self.desviacion = DesviacionIndicesVM()

    @execute_safely
    def calculate(self) -> None:
        df = self.indices.get_df()
        fecha = datetime.strptime(TODAY_DATE_FILE_YMD, FILE_STRFTIME_YMD).date()
        choices = ("Encima", "Muy por encima", "Igual", "Debajo", "Muy por debajo")

        agrupado_repuesto = df.groupby(["Cabecera", "TipoRepuesto"]).agg(
            {"ConsumoIndice":"mean"}
        ).rename(columns={"ConsumoIndice":"MediaRepuesto"}).reset_index()

        agrupado_cabecera = df.groupby(["Cabecera"]).agg(
            {"ConsumoIndice":"mean"}
        ).rename(columns={"ConsumoIndice": "MediaCabecera"}).reset_index()


        # Repuesto
        agrupado_repuesto["MediaDeMediasRepuesto"] = (
            agrupado_repuesto.groupby("TipoRepuesto")["MediaRepuesto"]
            .transform(lambda x: round(x.mean(), 2))
        )

        agrupado_repuesto["DiferenciaRepuesto"] = self.calc_diferencia(agrupado_repuesto["MediaRepuesto"],
                                                                       agrupado_repuesto["MediaDeMediasRepuesto"])
        agrupado_repuesto["DesviacionRepuesto"] = self.calc_desviacion(agrupado_repuesto["DiferenciaRepuesto"],
                                                                       agrupado_repuesto["MediaDeMediasRepuesto"])

        conditions = [
            (agrupado_repuesto["DesviacionRepuesto"] > 0) & (agrupado_repuesto["DesviacionRepuesto"] <= 50),
            (agrupado_repuesto["DesviacionRepuesto"] > 50),
            (agrupado_repuesto["DesviacionRepuesto"] == 0),
            (agrupado_repuesto["DesviacionRepuesto"] < 0) & (agrupado_repuesto["DesviacionRepuesto"] >= -50),
            (agrupado_repuesto["DesviacionRepuesto"] < -50)
        ]
        agrupado_repuesto["DesviacionRepuestoPor"] = np.select(conditions, choices, default="Debajo")


        # Cabecera
        agrupado_cabecera["MediaDeMediasCabecera"] = self.calc_media(agrupado_cabecera["MediaCabecera"])
        agrupado_cabecera["DiferenciaCabecera"] = self.calc_diferencia(agrupado_cabecera["MediaCabecera"],
                                                                       agrupado_cabecera["MediaDeMediasCabecera"])
        agrupado_cabecera["DesviacionCabecera"] = self.calc_desviacion(agrupado_cabecera["DiferenciaCabecera"],
                                                                       agrupado_cabecera["MediaDeMediasCabecera"])

        conditions = [
            (agrupado_cabecera["DesviacionCabecera"] > 0) & (agrupado_cabecera["DesviacionCabecera"] <= 50),
            (agrupado_cabecera["DesviacionCabecera"] > 50),
            (agrupado_cabecera["DesviacionCabecera"] == 0),
            (agrupado_cabecera["DesviacionCabecera"] < 0) & (agrupado_cabecera["DesviacionCabecera"] >= -50),
            (agrupado_cabecera["DesviacionCabecera"] < -50)
        ]
        agrupado_cabecera["DesviacionCabeceraPor"] = np.select(conditions, choices, default="Debajo")


        agrupado = pd.merge(agrupado_repuesto, agrupado_cabecera, on="Cabecera")
        agrupado["FechaCompleta"] = fecha

        self.desviacion.delete_all()
        self.desviacion.save_df(agrupado)


    @staticmethod
    def calc_diferencia(a, b):
        return round(a - b, 2)

    @staticmethod
    def calc_desviacion(c, b):
        return round((c / b) * 100, 2)

    @staticmethod
    def calc_media(a):
        return round(a.mean(),2)