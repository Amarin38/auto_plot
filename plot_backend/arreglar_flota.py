import pandas as pd

from numpy import ndarray
from typing import List, Union

class ArreglarFlota:
    def __init__(self, archivo: str) -> None:
        self.archivo = archivo
        self.cabecera = pd.read_excel(f"excel_info/internos_asignados_cabecera.xlsx")["Cabecera"].unique()

    def limpiar(self) -> pd.DataFrame:
        """
        Cleans the 'Flota'.xlsx files for statistics.
        """
        df: pd.DataFrame = pd.read_excel(f"excel/{self.archivo}.xlsx", engine="calamine")

        # el - es el "not"
        df = df.loc[-df["Motor modelo"].isin(["HTM3500", "SCANNIA 6 CIL", "DC 09 142 280CV", "MBENZ"]),
                    ["Linea", "Interno", "Dominio", "Chasis Modelo", "Chasis N°", 
                    "Chasis Año", "Motor modelo", "Motor N° de serie"]]

        df = df.drop(df.loc[
            (df["Chasis Año"].isin([0])) | 
            (df["Chasis Año"].isnull()) | 
            (df["Motor modelo"].isnull()) |
            (df["Motor modelo"] == "MWM MAXFOR 4 CIL") |
            (df["Motor modelo"] == "CUMMINS 4 CIL") |
            (df["Motor modelo"] == "MWM 6 CIL") |
            (df["Linea"].isin([300, 128, 158, 32, 75])) 
        ].index, axis=0)

        df.loc[
            (df["Chasis Año"] > 2016) & 
            (df["Chasis Modelo"].str.contains("27")) , 
            ["Motor modelo"]
        ] = "CUMMINS ISL MT27 6C"
        
        df.loc[
            (df["Chasis Año"] <= 2016) & 
            ((df["Motor modelo"] == "CUMMINS 6 CIL") | (df["Motor modelo"] == "CUMMINS 4 CIL")), 
            ["Motor modelo"]
        ] = "CUMMINS 4C/6C E3"
        
        df.loc[
            (df["Chasis Año"] > 2016) &
            (df["Motor modelo"].str.contains("CUMMINS 6")), 
            ["Motor modelo"]
        ] = "CUMMINS 6C EURO V"

        df.loc[
            (df["Motor modelo"].str.contains("MAXFOR 6")), 
            ["Motor modelo"]
        ] = "MAXXFORCE 6C"
        
        df.loc[
            (df["Motor modelo"].str.contains("MWM 4")), 
            ["Motor modelo"]
        ] = "MWM 4C"

        return df


    def asignar_cabecera(self) -> pd.DataFrame:
        """
        Assigns the 'Cabecera' to each 'Interno' number.
        """
        df: pd.DataFrame = self.limpiar()
        internos_cabecera: pd.DataFrame = pd.read_excel("excel_info/internos_asignados_cabecera.xlsx", engine="calamine")

        for cab in self.cabecera:
            internos = internos_cabecera.loc[internos_cabecera["Cabecera"] == cab, "Interno"].tolist() # type: ignore
            df.loc[df["Interno"].isin(internos), ["Cabecera"]] = cab # asigno la cabecera al interno # type: ignore

        # df.to_excel("internos_asignados.xlsx")
        return df


    def contar_motores_por_cabecera(self) -> pd.DataFrame:
        df_flota: pd.DataFrame = self.asignar_cabecera()
        dict_contado: List[Union[str, int]] = []
        
        repuestos: ndarray = df_flota["Motor modelo"].unique() 
        
        for cab in self.cabecera:
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
        df_contado.to_excel("motores_por_cabecera.xlsx")
        return df_contado


if __name__ == "__main__":
    limpiar = ArreglarFlota("flota7")
    limpiar.contar_motores_por_cabecera()
    