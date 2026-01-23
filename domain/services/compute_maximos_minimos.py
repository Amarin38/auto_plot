from typing import Optional

import pandas as pd

from utils.exception_utils import execute_safely
from viewmodels.maximos_minimos.vm import MaximosMinimosVM

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

            df_final = df_final[["Familia", "Articulo", "Repuesto", "Minimo", "Maximo"]]

            MaximosMinimosVM().save_df(df_final)
        