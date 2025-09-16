import pandas as pd

from src.utils.exception_utils import execute_safely
from src.db_data.crud_services import df_to_db, db_to_df

class FleetDataCleaner:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.cabecera = db_to_df("internos_asignados")


    @execute_safely
    def count_motors_by_cabecera(self) -> None:
        """
        ### Cuenta la cantidad de motores por cabecera y las asigna\n
        ### en un nuevo file separado por motor.
        """
        df_fleet: pd.DataFrame =  self.assign_cabecera() # type: ignore

        df_fleet["Motores"] = df_fleet["Motor modelo"]
        df_grouped = df_fleet.groupby(["Cabecera", "Motores"]).agg({"Motor modelo":"count"}).reset_index()
        df_grouped = df_grouped.rename(columns={"Motor modelo":"Cantidad Motores"})[["Cabecera", "Motores", "Cantidad Motores"]]

        df_to_db("motores_cabecera", df_grouped)


    @execute_safely
    def assign_cabecera(self) -> pd.DataFrame:
        """
        ### Asigna la 'Cabecera' a cada numero de 'Interno'.
        """
        df: pd.DataFrame = self.clean_fleet() # type: ignore

        columns = self.cabecera[["Cabecera", "Interno"]]
        merged = df.merge(columns)

        return merged


    @execute_safely
    def clean_fleet(self) -> pd.DataFrame:
        """
        ### Cleans the 'Flota'.xlsx files for statistics.
        """
        self.df = self.df.loc[~self.df["Motor modelo"].isin(["HTM3500", "SCANNIA 6 CIL", "DC 09 142 280CV", "MBENZ"]), # type: ignore
                              ["Linea", "Interno", "Dominio", "Chasis Modelo", "Chasis N°", 
                               "Chasis Año", "Motor modelo", "Motor N° de serie"]]

        self.df = self.df.drop(self.df.loc[
            (self.df["Chasis Año"].isin([0])) | 
            (self.df["Chasis Año"].isnull()) | 
            (self.df["Motor modelo"].isnull()) |
            (self.df["Motor modelo"] == "MWM MAXFOR 4 CIL") |
            (self.df["Motor modelo"] == "CUMMINS 4 CIL") |
            (self.df["Motor modelo"] == "MWM 6 CIL") |
            (self.df["Linea"].isin([300, 128, 158, 32, 75])) 
        ].index, axis=0)

        self.df.loc[
            (self.df["Chasis Año"] > 2016) & 
            (self.df["Chasis Modelo"].str.contains("27")), 
            ["Motor modelo"]
        ] = "CUMMINS ISL MT27 6C"
        
        self.df.loc[
            (self.df["Chasis Año"] <= 2016) & 
            ((self.df["Motor modelo"] == "CUMMINS 6 CIL") | (self.df["Motor modelo"] == "CUMMINS 4 CIL")), 
            ["Motor modelo"]
        ] = "CUMMINS 4C/6C E3"
        
        self.df.loc[
            (self.df["Chasis Año"] > 2016) &
            (self.df["Motor modelo"].str.contains("CUMMINS 6")), 
            ["Motor modelo"]
        ] = "CUMMINS 6C EURO V"

        self.df.loc[
            (self.df["Motor modelo"].str.contains("MAXFOR 6")), 
            ["Motor modelo"]
        ] = "MAXXFORCE 6C"
        
        self.df.loc[
            (self.df["Motor modelo"].str.contains("MWM 4")), 
            ["Motor modelo"]
        ] = "MWM 4C"

        return self.df
    