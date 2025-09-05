from typing import List, Optional
from enum import Enum
from src.services.scrapping.scrap_maxmin import ScrapMaxMin


class ScrapEnum(Enum):
    WEB_SCRAP = "web"
    LOCAL_SCRAP = "local"

class ExcelEnum(Enum):
    WITH_EXCEL = "con excel"
    WITHOUT_EXCEL = "sin excel"

    
class MaxMinUtils:
    def create_code_list(self, date_since: str, with_excel: str = "sin excel", scrap: str = "web") -> Optional[List[tuple]]:
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
