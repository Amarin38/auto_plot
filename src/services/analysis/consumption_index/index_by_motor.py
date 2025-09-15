import pandas as pd
import numpy as np

from typing import List, Union

from src.config.constants import OUT_PATH
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.db.crud_services import CRUDServices

class IndexByMotor:
    def __init__(self) -> None:
        self.df_motors = CRUDServices().db_to_df("motores_cabecera")


    def calculate_index(self, df: pd.DataFrame, tipo: str) -> List[Union[pd.DataFrame, str]]:
        grouped = df.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum'}).reset_index()

        df_with_vehicles = grouped.merge(self.df_motors, on=["Cabecera", "Repuesto"], how="right") # hago join con la cantidad de coches para hacer el cálculo
        df_with_vehicles["IndiceConsumo"] = round((df_with_vehicles["Cantidad"]*100) / df_with_vehicles["CantidadMotores"], 1) # hago el cálculo y se lo asigno a una nueva columna

        df_rate = df_with_vehicles[['Cabecera', 'Repuesto', 'IndiceConsumo']]
        df_rate["IndiceConsumo"].replace([np.inf, -np.inf], np.nan, inplace=True)
        df_rate.dropna(subset=["IndiceConsumo"], inplace=True)
        df_rate.insert(2, 'TipoRepuesto', tipo)
        
        return [df_rate, self._create_title_date(df)]


    @staticmethod
    def _create_title_date(df: pd.DataFrame) -> str:
        """
        Devuelve la fecha del titulo basandose en el file introducido.
        """
        dates = df["Fecha"].unique()
        return f"{dates.min()} a {dates.max()}"
