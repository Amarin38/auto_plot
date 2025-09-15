import json

import pandas as pd

from typing import Dict

from src.config.constants import TODAY_FOR_DELTA
from src.db.crud_common import CRUDCommon

class IndexGomeria:
    def __init__(self, file: str, diff_months: int) -> None:
        self.file = file
        self.diff_months = diff_months



    # def calculate_trend(self) -> None: #FIXME:
    #     df = pd.read_excel(f"{self.file}.xlsx", engine="calamine")
    #     with open(f"{}/meses.json", "r") as m:
    #         meses: Dict[str,int] = json.load(m)

    #     consumo_cantidad: Dict[str, int] = {}
    #     consumo_coste: Dict[str, float] = {}
        
    #     for mes, num_mes in meses.items():
    #         df_filtrado = df[df["FechaCompleta"].dt.month == num_mes] # separo por mes

    #         cantidad_total_por_mes = df.iloc[df_filtrado.index, 11].sum() # sumo consumo en ese mes
    #         precio_total_por_mes = (df.iloc[df_filtrado.index, 11] * df.iloc[df_filtrado.index, 13]).sum() # sumo el consumo en plata en ese mes 

    #         consumo_cantidad.update({mes:int(cantidad_total_por_mes)})
    #         consumo_coste.update({mes:round(float(precio_total_por_mes),2)})
        
    #     df_final: pd.DataFrame = pd.DataFrame({"Cantidad":[consumo_cantidad],
    #                                            "Coste":[consumo_coste]})
        
    #     df_final.to_excel(f"{EXCEL_PATH}/cubiertas_consumo_{self.file}.xlsx")


    def update_tire_values(self) -> Dict[str, float]: # FIXME:
        meses: pd.Index = self._create_months_list(self.diff_months)
        indice_consumo_por_mes: Dict[str, float] = {}

        # data_consumo = pd.read_excel(f"{EXCEL_PATH}/cubiertas_consumo_{self.file}.xlsx", engine="calamine")
        data_armadas = CRUDCommon().read_json_config("cubiertas_armadas")

        # for mes in meses:
        #     total_consumo = round(data_consumo["plata"][0][mes]/data_armadas["cantidad"][0][mes], 2) 
        #     indice_consumo_por_mes.update({mes:total_consumo})
        
        return indice_consumo_por_mes


    @staticmethod
    def _create_months_list(diff_months) -> pd.Index:
        diff = pd.date_range(TODAY_FOR_DELTA - pd.Timedelta(days=30*diff_months))

        return pd.DatetimeIndex(diff.strftime("%Y-%B").unique())