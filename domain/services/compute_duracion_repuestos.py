import numpy as np
import pandas as pd
from scipy.stats import norm

from config.constants_cleaner import FILTRO_OBS
from utils.exception_utils import execute_safely
from viewmodels.consumo.duracion_rep.distri_normal_vm import DistribucionNormalVM
from viewmodels.consumo.duracion_rep.duracion_vm import DuracionRepuestosVM


class DuracionRepuestos:
    def __init__(self, df: pd.DataFrame, repuesto_rep: str, tipo_duracion: str) -> None:
        self.df         = df
        self.repuesto   = repuesto_rep
        self.tipo_rep   = tipo_duracion

        self.patentes   = self.df["Patente"].unique()
        self.cabeceras  = self.df["Cabecera"].unique()


    @execute_safely
    def calcular_duracion(self):
        df = self.df.loc[
             self.df["Observaciones"].str.contains(FILTRO_OBS, na=False)
        ].copy()

        # Vectorización de la duración y el número de cambio
        df = df.sort_values(by=["Patente", "FechaCambio"]).reset_index(drop=True)
        df["Cambio"] = df.groupby("Patente").cumcount()
        df["DuracionEnDias"] = df.groupby("Patente")["FechaCambio"].diff().dt.days.fillna(0).astype(int)
        
        df["Repuesto"] = self.repuesto
        df["TipoRepuesto"] = self.tipo_rep

        # Limpieza de valores
        df.loc[df["DuracionEnDias"] < 0, "DuracionEnDias"] = 0

        df["DuracionEnMeses"]   = round(df["DuracionEnDias"] / 30, 1)
        df["DuracionEnAños"]    = round(df["DuracionEnDias"] / 365, 1)
        df["FechaCambio"]       = df["FechaCambio"].dt.date

        cambios = df["Cambio"].unique()[1:]

        df_duracion = self.calcular_media_y_std(df, cambios)

        if df_duracion["Cabecera"].isna().any():
            df_distribucion_normal = self.calcular_distribucion_normal(df_duracion, cambios)
        else:
            df_distribucion_normal = self.calcular_distribucion_normal_cabecera(df_duracion, cambios)

        DuracionRepuestosVM().save_df(df_duracion)
        DistribucionNormalVM().save_df(df_distribucion_normal)


    @execute_safely
    def calcular_distribucion_normal(self, df: pd.DataFrame, cambios) -> pd.DataFrame:
        df_list = []

        grouped_cambio = df.groupby("Cambio")

        for cambio in cambios:
            df_final = pd.DataFrame()
            df_cambio = grouped_cambio.get_group(cambio)

            # Gauss
            mu      = df_cambio["AñoPromedio"].iloc[0]
            sigma   = df_cambio["desviacion_indicestandar"].iloc[0]
            x       = np.arange(1, 16)

            # Creo el DataFrame
            df_final["Años"]                      = x
            df_final["Cambio"]                    = cambio
            df_final["Repuesto"]                  = self.repuesto
            df_final["TipoRepuesto"]              = self.tipo_rep
            df_final["AñoPromedio"]               = mu
            df_final["desviacion_indicestandar"]  = sigma
            df_final["DistribucionNormal"]        = (norm.pdf(x, mu, sigma).round(2)) * 100
            df_final["DistribucionNormal"]        = df_final["DistribucionNormal"].fillna(0)

            df_list.append(df_final)
        return pd.concat(df_list)


    @execute_safely
    def calcular_media_y_std(self, df: pd.DataFrame, cambios) -> pd.DataFrame:
        # Vectorización del cálculo de media y std
        df["AñoPromedio"] = df.groupby("Cambio")["DuracionEnAños"].transform("mean").round(1)
        df["desviacion_indicestandar"] = df.groupby("Cambio")["DuracionEnAños"].transform("std").round(1)

        df["AñoPromedio"] = df["AñoPromedio"].fillna(0)
        df["desviacion_indicestandar"] = df["desviacion_indicestandar"].fillna(0)

        return df


    @execute_safely
    def calcular_distribucion_normal_cabecera(self, df: pd.DataFrame, cambios) -> pd.DataFrame:
        df_list = []

        for cambio in cambios:
            for cab in self.cabeceras:
                df_aux = pd.DataFrame()
                mask = (df["Cambio"] == cambio) & (df["Cabecera"] == cab)
                
                # Gauss
                mu = df.loc[mask, "AñoPromedio"].iloc[0] if not df.loc[mask].empty else 0
                sigma = df.loc[mask, "desviacion_indicestandar"].iloc[0] if not df.loc[mask].empty else 0

                x = np.arange(1, 16)

                if mu != 0 and sigma != 0:
                    distribucion_normal = (norm.pdf(x, mu, sigma).round(2)) * 100
                else:
                    distribucion_normal = 0

                # Creo el DataFrame
                df_aux["Años"]                      = x
                df_aux["Cambio"]                    = cambio
                df_aux["Cabecera"]                  = cab
                df_aux["Repuesto"]                  = self.repuesto
                df_aux["TipoRepuesto"]              = self.tipo_rep
                df_aux["AñoPromedio"]               = mu
                df_aux["desviacion_indicestandar"]  = sigma
                df_aux["DistribucionNormal"]        = distribucion_normal
                df_aux["DistribucionNormal"]        = df_aux["DistribucionNormal"].fillna(0)

                df_list.append(df_aux)
        return pd.concat(df_list)


    @execute_safely
    def calcular_media_y_std_cabecera(self, df: pd.DataFrame, cambios) -> pd.DataFrame:
        # Vectorización del cálculo de media y std por cabecera
        df["AñoPromedio"] = df.groupby(["Cambio", "Cabecera"])["DuracionEnAños"].transform("mean").round(1)
        df["desviacion_indicestandar"] = df.groupby(["Cambio", "Cabecera"])["DuracionEnAños"].transform("std").round(1)

        df["AñoPromedio"] = df["AñoPromedio"].fillna(0)
        df["desviacion_indicestandar"] = df["desviacion_indicestandar"].fillna(0)

        return df
