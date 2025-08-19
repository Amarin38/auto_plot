import pandas as pd


from config.constants import MAIN_PATH
from services.utils.general_utils import GeneralUtils

class ArreglarFlota:
    def __init__(self, file: str) -> None:
        self.df = GeneralUtils(file).convert_to_df()
        self.cabecera = pd.read_excel(f"{MAIN_PATH}/src/data/excel_data/internos_asignados_cabecera.xlsx")


    def contar_motores_por_cabecera(self) -> None:
        """
        ### Cuenta la cantidad de motores por cabecera y las asigna\n
        ### en un nuevo archivo separado por motor.
        """
        df_flota: pd.DataFrame =  self.asignar_cabecera()

        df_flota["Motores"] = df_flota["Motor modelo"]
        df_agrupado = df_flota.groupby(["Cabecera", "Motores"]).agg({"Motor modelo":"count"}).reset_index()
        df_agrupado = df_agrupado.rename(columns={"Motor modelo":"Cantidad Motores"})[["Cabecera", "Motores", "Cantidad Motores"]]
        df_agrupado.to_excel(f"{MAIN_PATH}/src/data/excel_data/motores_por_cabecera.xlsx")


    def asignar_cabecera(self) -> pd.DataFrame:
        """
        ### Asigna la 'Cabecera' a cada numero de 'Interno'.
        """
        df: pd.DataFrame = self.limpiar_flota()

        columnas = self.cabecera[["Cabecera", "Interno"]]
        merged = df.merge(columnas)

        return merged


    def limpiar_flota(self) -> pd.DataFrame:
        """
        ### Cleans the 'Flota'.xlsx files for statistics.
        """
        # el - es el "not"
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
    