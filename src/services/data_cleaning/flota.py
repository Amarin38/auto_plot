import pandas as pd

from numpy import ndarray
from typing import List, Union

from plot_backend.utils.general_utils import GeneralUtils
from src.config.constants import MAIN_PATH

class ArreglarFlota:
    def __init__(self, file: str) -> None:
        self.df = GeneralUtils(file).check_filetype()
        self.cabecera = pd.read_excel(f"{MAIN_PATH}/excel_info/internos_asignados_cabecera.xlsx")["Cabecera"]


    def contar_motores_por_cabecera(self) -> pd.DataFrame:
        """
        ### Cuenta la cantidad de motores por cabecera y las asigna\n
        ### en un nuevo archivo separado por motor.
        """
        df_flota: pd.DataFrame = self.asignar_cabecera()
        dict_contado: List[Union[str, int]] = []
        
        repuestos: ndarray = df_flota["Motor modelo"].unique() 
        
        for cab in self.cabecera.unique():
            for rep in repuestos:
                rep_comparado: bool = df_flota["Motor modelo"] == rep
                cab_comparada: bool = df_flota["Cabecera"] == cab

                cantidad_rep = df_flota.loc[rep_comparado & cab_comparada, ["Motor modelo"]].count().iloc[0] # type:ignore

                dict_contado.append({
                    "Cabecera":cab,
                    "Repuesto":rep,
                    "Cantidad":int(cantidad_rep)
                }) # type: ignore
            
        df_contado: pd.DataFrame = pd.DataFrame(dict_contado)
        # df_contado.to_excel(f"{self._main_path}/excel_info/motores_por_cabecera.xlsx")
        return df_contado


    def asignar_cabecera(self) -> pd.DataFrame:
        """
        ### Asigna la 'Cabecera' a cada numero de 'Interno'.
        """
        df: pd.DataFrame = self.limpiar_flota()

        for cab in self.cabecera.unique():
            internos = self.cabecera.loc[self.cabecera["Cabecera"] == cab, 
                                         "Interno"].tolist() # type: ignore
            df.loc[df["Interno"].isin(internos), 
                   ["Cabecera"]] = cab # asigno la cabecera al interno # type: ignore

        # self.df.to_excel(f"{self._main_path}/out/internos_asignados.xlsx")
        return df


    def limpiar_flota(self) -> pd.DataFrame:
        """
        ### Cleans the 'Flota'.xlsx files for statistics.
        """
        # el - es el "not"
        self.df = self.df.loc[-self.df["Motor modelo"].isin(["HTM3500", "SCANNIA 6 CIL", "DC 09 142 280CV", "MBENZ"]), # type: ignore
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
            (self.df["Chasis Modelo"].str.contains("27")) , 
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
    