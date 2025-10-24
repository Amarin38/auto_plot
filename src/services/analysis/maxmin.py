from typing import List, Optional

import pandas as pd

from src.config.enums import ScrapEnum
from src.db_data.crud_services import df_to_db
from src.services.scrapping.scrap_maxmin import ScrapMaxMin
from src.utils.exception_utils import execute_safely

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maxmin.
- Se procesa el file y quedan solo las salidas.
- Se pasa por el programa
"""


class MaxMin:
    @execute_safely
    def calculate(self, df: Optional[pd.DataFrame] = None, mult_por_min: float = 2.5, mult_por_max: float = 4) -> None:
        if df is not None:
            df_final = df.groupby(["Familia", "Articulo", "Repuesto"]).agg({"Cantidad":"sum"}).reset_index()
            div_seis_meses = round(df_final["Cantidad"] / 6, 1)

            df_final["Minimo"] = div_seis_meses * mult_por_min
            df_final["Maximo"] = div_seis_meses * mult_por_max
        
            df_final = df_final[["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"]]
            
            df_to_db("maxmin", df_final)


    @staticmethod
    @execute_safely
    def _create_code_list(date_since: str, scrap: ScrapEnum = ScrapEnum.WEB) -> Optional[List[tuple]]:
        """
        Genera automáticamente la lista de códigos a los que sacarles el máximo y mínimo.\n
        Args:\n
            with_excel (str):\n
            ["con excel", "sin excel"]\n

        Returns:\n
            Optional[str]: None | lista de codigos de maxmin\n
        """
        lista_codigos: List[str] = []
        match scrap:
            case ScrapEnum.WEB: lista_codigos = ScrapMaxMin(date_since).web()
            case ScrapEnum.LOCAL: lista_codigos = ScrapMaxMin(date_since).local()

        return [tuple(map(int, codigo.split("."))) for codigo in lista_codigos]
        