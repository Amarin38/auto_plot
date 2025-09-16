import pandas as pd

from typing import List, Optional

from src.config.enums import ScrapEnum

from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.scrapping.scrap_maxmin import ScrapMaxMin 

from src.utils.exception_utils import execute_safely

from src.db.crud_services import df_to_db

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maxmin.
- Se procesa el file y quedan solo las salidas.
- Se pasa por el programa
"""


class MaxMin:
    @execute_safely
    def calculate(self, df: Optional[pd.DataFrame] = None, multiplicar_por: float = 2.5) -> None:
        if df is not None:
            df_final = df.groupby(["Familia", "Articulo", "Repuesto"]).agg({"Cantidad":"sum"}).reset_index()
            
            minimo: pd.Series[float] = round((df_final["Cantidad"] / 6) * multiplicar_por, 1)
            maximo: pd.Series[float] = minimo * 2

            df_final["Minimo"] = minimo
            df_final["Maximo"] = maximo
        
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
        match scrap:
            case ScrapEnum.WEB: lista_codigos = ScrapMaxMin(date_since).web()
            case ScrapEnum.LOCAL: lista_codigos = ScrapMaxMin(date_since).local()

        return [tuple(map(int, codigo.split("."))) for codigo in lista_codigos]
        