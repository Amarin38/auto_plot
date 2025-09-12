import pandas as pd

from typing import List, Optional, Literal
from datetime import datetime, timedelta
from io import BytesIO

from src.config.constants import MAIN_PATH
from src.config.enums import ScrapEnum, ExcelEnum

from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.utils.exception_utils import execute_safely
from src.utils.common_utils import CommonUtils
from src.services.scrapping.scrap_maxmin import ScrapMaxMin 

from src.db.crud import df_to_sql, sql_to_df

"""
- Se descargan los consumos de x fecha hacia atrás de los productos que se queira evaluar el  maxmin.
- Se procesa el file y quedan solo las salidas.
- Se pasa por el programa
"""


class MaxMin:
    def __init__(self) -> None:
        self.data_cleaner = InventoryDataCleaner()
        self.common = CommonUtils()


    @execute_safely
    def create_maxmin(self, directory: str = "todo maxmin") -> pd.DataFrame:
        dir_exists = self.common.check_dir_exists(MAIN_PATH, directory)
        fecha = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        
        if dir_exists:
            self._create_code_list(fecha)
            return self.calculate()
        else:
            return sql_to_df("maxmin")


    @execute_safely
    def calculate(self, directory: str = "todo maxmin", multiplicar_por: float = 2.5) -> pd.DataFrame:
        df = self.data_cleaner.run_all(directory)
        
        df_agrupado: pd.DataFrame = df.groupby(["Familia", "Articulo", "Repuesto"]).agg({"Cantidad":"sum"}).reset_index()
        min_calc: pd.Series[float] = round(df_agrupado["Cantidad"] / 6, 1) * multiplicar_por

        df_agrupado["Minimo"] = min_calc
        df_agrupado["Maximo"] = min_calc * 2
    
        df_agrupado = df_agrupado[["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"]]

        df_to_sql("maxmin", df_agrupado)
        return df_agrupado



    @staticmethod
    @execute_safely
    def _create_code_list(date_since: str, with_excel: Literal["WITH EXCEL", "WITHOUT EXCEL"] = "WITHOUT EXCEL", scrap: Literal["WEB", "LOCAL"] = "WEB") -> Optional[List[tuple]]:
        """
        Genera automáticamente la lista de códigos a los que sacarles el máximo y mínimo.\n
        Args:\n
            with_excel (str):\n
            ["con excel", "sin excel"]\n

        Returns:\n
            Optional[str]: None | lista de codigos de maxmin\n
        """
        if scrap == ScrapEnum.WEB_SCRAP.value:
            lista_codigos = ScrapMaxMin(date_since).web()
        elif scrap == ScrapEnum.LOCAL_SCRAP.value:
            lista_codigos = ScrapMaxMin(date_since).local()

        lista_final: List[tuple] = [tuple(map(int, codigo.split("."))) for codigo in lista_codigos]
        
        if with_excel == ExcelEnum.WITH_EXCEL.value:
            import pandas as pd

            df = pd.DataFrame({
                "Familia":[fam[0] for fam in lista_final], 
                "Articulo":[art[1] for art in lista_final]
                })
            df.to_excel(f"codigos_maxmin.xlsx")
        elif with_excel == ExcelEnum.WITHOUT_EXCEL.value:
            return lista_final
        else:
            raise ValueError("Solo se puede con o sin excel")