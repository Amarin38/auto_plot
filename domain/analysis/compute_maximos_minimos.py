from typing import List, Optional

import pandas as pd

from config.enums import ScrapEnum
from infrastructure.db.crud_services import df_to_db
from domain.scraping.scrap_maximos_minimos import ScrapMaxMin
from utils.exception_utils import execute_safely

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maximos_minimos.
- Se procesa el file y quedan solo las salidas.
- Se pasa por el programa
"""


class MaxMin:
    @execute_safely
    def calculate(self, df: Optional[pd.DataFrame] = None, mult_por_min: float = 2, mult_por_max: float = 3) -> None:
        if df is not None:
            df_final = df.groupby(["Familia", "Articulo", "Repuesto"]).agg({"Cantidad":"sum"}).reset_index()
            div_seis_meses = round(df_final["Cantidad"] / 6, 1)

            df_final["Minimo"] = round(div_seis_meses * mult_por_min, 1)
            df_final["Maximo"] = round(div_seis_meses * mult_por_max, 1)

            # print(div_seis_meses.loc[(df_final["Familia"] == 112) & (df_final["Articulo"] == 23)])

            df_final = df_final[["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"]]
            
            df_to_db("maximos_minimos", df_final)


    @staticmethod
    @execute_safely
    def _create_code_list(date_since: str, scrap: ScrapEnum = ScrapEnum.WEB) -> Optional[List[tuple]]:
        """
        Genera automáticamente la lista de códigos a los que sacarles el máximo y mínimo.\n
        Args:\n
            with_excel (str):\n
            ["con excel", "sin excel"]\n

        Returns:\n
            Optional[str]: None | lista de codigos de maximos_minimos\n
        """
        lista_codigos: List[str] = []
        match scrap:
            case ScrapEnum.WEB: lista_codigos = ScrapMaxMin(date_since).web()
            case ScrapEnum.LOCAL: lista_codigos = ScrapMaxMin(date_since).local()

        return [tuple(map(int, codigo.split("."))) for codigo in lista_codigos]
        