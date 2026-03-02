import pandas as pd

from utils.exception_utils import execute_safely


class FleetDataCleaner:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df


    @execute_safely
    def count_motors_by_cabecera(self) -> None:
        """
        ### Cuenta la cantidad de motor por cabecera y las asigna\n
        ### en un nuevo file separado por motor.
        """
        df_fleet: pd.DataFrame =  self.assign_cabecera() # type: ignore

        df_fleet["Motores"] = df_fleet["Motor modelo"]
        df_grouped = df_fleet.groupby(["Cabecera", "Motores"]).agg({"Motor modelo":"count"}).reset_index()
        df_grouped = df_grouped.rename(columns={"Motor modelo":"Cantidad Motores"})[["Cabecera", "Motores", "Cantidad Motores"]]

        return df_grouped


    @execute_safely
    def assign_cabecera(self) -> pd.DataFrame:
        """
        ### Asigna la 'Cabecera' a cada numero de 'Interno'.
        """
        df: pd.DataFrame = self.clean_fleet() # type: ignore

        columns = self.df[["Cabecera", "Interno"]]
        merged = df.merge(columns)

        return merged


    @execute_safely
    def clean_fleet(self) -> pd.DataFrame:
        """
        ### Cleans the 'Flota'.xlsx files for statistics.
        """
        motores_excluidos = ["HTM3500", "SCANNIA 6 CIL", "DC 09 142 280CV", "MBENZ"]
        columnas_interes = ["Linea", "Interno", "Dominio", "Chasis Modelo", "Chasis N°", 
                            "Chasis Año", "Motor modelo", "Motor N° de serie"]
        
        self.df = self.df.loc[~self.df["Motor modelo"].isin(motores_excluidos), columnas_interes]

        condiciones_eliminar = (
            (self.df["Chasis Año"].isin([0])) | 
            (self.df["Chasis Año"].isnull()) | 
            (self.df["Motor modelo"].isnull()) |
            (self.df["Motor modelo"].isin(["MWM MAXFOR 4 CIL", "CUMMINS 4 CIL", "MWM 6 CIL"])) |
            (self.df["Linea"].isin([300, 128, 158, 32, 75]))
        )
        
        self.df = self.df.loc[~condiciones_eliminar]

        mask_mt27       = ((self.df["Chasis Año"] > 2016) &
                           (self.df["Chasis Modelo"].str.contains("27", na=False)))
        mask_e3         = ((self.df["Chasis Año"] <= 2016) &
                           (self.df["Motor modelo"].isin(["CUMMINS 6 CIL", "CUMMINS 4 CIL"])))
        mask_euro_v     = ((self.df["Chasis Año"] > 2016) &
                           (self.df["Motor modelo"].str.contains("CUMMINS 6", na=False)))
        mask_maxxforce  = self.df["Motor modelo"].str.contains("MAXFOR 6", na=False)
        mask_mwm        = self.df["Motor modelo"].str.contains("MWM 4", na=False)

        self.df.loc[mask_mt27, "Motor modelo"] = "CUMMINS ISL MT27 6C"
        self.df.loc[mask_e3, "Motor modelo"] = "CUMMINS 4C/6C E3"
        self.df.loc[mask_euro_v, "Motor modelo"] = "CUMMINS 6C EURO V"
        self.df.loc[mask_maxxforce, "Motor modelo"] = "MAXXFORCE 6C"
        self.df.loc[mask_mwm, "Motor modelo"] = "MWM 4C"

        return self.df
