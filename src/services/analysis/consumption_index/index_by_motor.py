import pandas as pd
import numpy as np

from typing import List, Union

from src.config.constants import OUT_PATH
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.db.crud import sql_to_df

class IndexByMotor:
    def __init__(self, file: str, directory: str, tipo: str) -> None:
        self.file = file
        self.directory = directory
        self.tipo = tipo
        self.df_motors = sql_to_df("motores_cabecera")
        self.df_consumption = pd.read_excel(f"{OUT_PATH}/{self.file}-S.xlsx", engine="calamine")


    def calculate_index(self) -> List[Union[pd.DataFrame, str]]:
        InventoryDataCleaner().run_all(self.directory)

        grouped = self.df_consumption.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum'}).reset_index()

        df_with_vehicles = grouped.merge(self.df_motors, on=["Cabecera", "Repuesto"], how="right") # hago join con la cantidad de coches para hacer el cálculo
        df_with_vehicles["IndiceConsumo"] = round((df_with_vehicles["Cantidad"]*100) / df_with_vehicles["CantidadMotores"], 1) # hago el cálculo y se lo asigno a una nueva columna

        df_rate = df_with_vehicles[['Cabecera', 'Repuesto', 'IndiceConsumo']]
        df_rate["IndiceConsumo"].replace([np.inf, -np.inf], np.nan, inplace=True)
        df_rate.dropna(subset=["IndiceConsumo"], inplace=True)
        df_rate.insert(2, 'TipoRepuesto', self.tipo)
        
        df_rate.to_excel(f"{OUT_PATH}/{self.file}_indice_por_motor.xlsx")
        return [df_rate, self._create_title_date(self.df_consumption)]


    @staticmethod
    def _create_title_date(df: pd.DataFrame) -> str:
        """
        Devuelve la fecha del titulo basandose en el file introducido.
        """
        dates = df["Fecha"].unique()
        return f"{dates.min()} a {dates.max()}"
