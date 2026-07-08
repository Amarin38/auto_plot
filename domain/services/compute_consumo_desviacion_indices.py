from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

from config.constants_common import TODAY_DATE_FILE_YMD, FILE_STRFTIME_YMD, CONSUMO_DESVIACION_CAB_COLS_RENAME, \
    CONSUMO_DESVIACION_REP_COLS_RENAME, DESVIACIONES_CHOICES
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

        agrupado_repuesto = df.groupby(["Cabecera", "TipoRepuesto"]).agg({"ConsumoIndice":"mean"}
        ).rename(columns=CONSUMO_DESVIACION_REP_COLS_RENAME).reset_index()

        agrupado_cabecera = df.groupby(["Cabecera"]).agg(
            {"ConsumoIndice":"mean"}
        ).rename(columns=CONSUMO_DESVIACION_CAB_COLS_RENAME).reset_index()


        # Repuesto
        agrupado_repuesto["MediaDeMediasRepuesto"] = (
            agrupado_repuesto.groupby("TipoRepuesto")["MediaRepuesto"]
            .transform(lambda x: round(x.mean(), 2))
        )

        agrupado_repuesto["DiferenciaRepuesto"] = agrupado_repuesto["MediaRepuesto"] - agrupado_repuesto["MediaDeMediasRepuesto"]
        agrupado_repuesto["DesviacionRepuesto"] = self.calc_desviacion(agrupado_repuesto["DiferenciaRepuesto"],
                                                                       agrupado_repuesto["MediaDeMediasRepuesto"])

        conditions = self.get_conditions(agrupado_repuesto, "DesviacionRepuesto")
        agrupado_repuesto["DesviacionRepuestoPor"] = np.select(conditions, DESVIACIONES_CHOICES, default="Debajo")


        # Cabecera
        agrupado_cabecera["MediaDeMediasCabecera"] = agrupado_cabecera["MediaCabecera"].mean()
        agrupado_cabecera["DiferenciaCabecera"] = agrupado_cabecera["MediaCabecera"] - agrupado_cabecera["MediaDeMediasCabecera"]
        agrupado_cabecera["DesviacionCabecera"] = self.calc_desviacion(agrupado_cabecera["DiferenciaCabecera"],
                                                                       agrupado_cabecera["MediaDeMediasCabecera"])

        conditions = self.get_conditions(agrupado_cabecera, "DesviacionCabecera")
        agrupado_cabecera["DesviacionCabeceraPor"] = np.select(conditions, DESVIACIONES_CHOICES, default="Debajo")

        agrupado = pd.merge(agrupado_repuesto, agrupado_cabecera, on="Cabecera")
        agrupado["FechaCompleta"] = fecha

        self.desviacion.delete_all()
        self.desviacion.save_df(agrupado)


    @staticmethod
    def calc_desviacion(c, b):
        return round(c / b) * 100


    @staticmethod
    def get_conditions(df_agrupado: pd.DataFrame, col: str) -> List[bool]:
        return [
            (df_agrupado[col] > 0) & (df_agrupado[col] <= 50),
            (df_agrupado[col] > 50),
            (df_agrupado[col] == 0),
            (df_agrupado[col] < 0) & (df_agrupado[col] >= -50),
            (df_agrupado[col] < -50)
        ]