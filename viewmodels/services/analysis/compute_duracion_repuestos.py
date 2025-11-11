import numpy as np
import pandas as pd
from scipy.stats import norm

from config.constants import FILTRO_OBS
from utils.exception_utils import execute_safely
from viewmodels.distribucion_normal_vm import DistribucionNormalVM
from viewmodels.duracion_repuestos_vm import DuracionRepuestosVM


class DuracionRepuestos:
    def __init__(self, df: pd.DataFrame, repuesto_rep: str, tipo_duracion: str) -> None:
        self.df = df
        self.repuesto = repuesto_rep
        self.tipo_rep = tipo_duracion

        self.patentes = self.df["Patente"].unique()
        self.cabeceras = self.df["Cabecera"].unique()


    @execute_safely
    def calcular_duracion(self):
        df = self.df.loc[self.df["Observaciones"].str.contains(FILTRO_OBS, na=False)].copy()

        for patente in self.patentes:
            df_separado_pat = df["Patente"] == patente

            # Separo por cada patende y traigo la columna Cambio, y a esa columna en ese espacio
            # Le aplico el rango del tamaño de ese sub-dataframe
            df.loc[df_separado_pat, "Cambio"] = range( # type: ignore
                len(df.loc[df_separado_pat])
            )
            df["Repuesto"] = self.repuesto
            df["TipoRepuesto"] = self.tipo_rep

            # Resto las fechas para saber cuanto duraron
            df.loc[df_separado_pat, "DuracionEnDias"] = df["FechaCambio"] - df["FechaCambio"].shift(1)

        df["Cambio"] = df["Cambio"].astype(int)

        df["DuracionEnDias"] = df["DuracionEnDias"].dt.days.fillna(0).astype(int) # limpio de valores nulos
        df.loc[df["DuracionEnDias"] < 0, "DuracionEnDias"] = 0 # limpio de valores negativos

        df["DuracionEnMeses"] = round(df["DuracionEnDias"] / 30, 1)
        df["DuracionEnAños"] = round(df["DuracionEnDias"] / 365, 1)
        df["FechaCambio"] = df["FechaCambio"].dt.date

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

        for cambio in cambios:
            df_aux = pd.DataFrame()
            df_cambio = df["Cambio"] == cambio

            # Gauss
            mu = df.loc[df_cambio, "AñoPromedio"].values[0] # type: ignore
            sigma = df.loc[df_cambio, "desviacion_indicestandar"].values[0] # type: ignore
            x = np.arange(1, 16)

            # Creo el DataFrame
            df_aux["Años"] = x
            df_aux["Cambio"] = cambio
            df_aux["Repuesto"] = self.repuesto
            df_aux["TipoRepuesto"] = self.tipo_rep
            df_aux["AñoPromedio"] = mu
            df_aux["desviacion_indicestandar"] = sigma
            df_aux["DistribucionNormal"] = (norm.pdf(x, mu, sigma).round(2)) * 100
            df_aux["DistribucionNormal"] = df_aux["DistribucionNormal"].fillna(0)

            df_list.append(df_aux)
        return pd.concat(df_list)


    @execute_safely
    def calcular_media_y_std(self, df: pd.DataFrame, cambios) -> pd.DataFrame:
        for cambio in cambios:
            df_cambio = df["Cambio"] == cambio

            df.loc[df_cambio, "AñoPromedio"] = df.loc[df_cambio, "DuracionEnAños"].mean()
            df.loc[df_cambio, "desviacion_indicestandar"] = df.loc[df_cambio, "DuracionEnAños"].std(ddof=1) #std de muestreo

        df["AñoPromedio"] = df["AñoPromedio"].fillna(0).round(1)
        df["desviacion_indicestandar"] = df["desviacion_indicestandar"].fillna(0).round(1)

        return df


    @execute_safely
    def calcular_distribucion_normal_cabecera(self, df: pd.DataFrame, cambios) -> pd.DataFrame:
        df_list = []

        for cambio in cambios:
            df_cambio: pd.Series[bool] = df["Cambio"] == cambio
            for cab in self.cabeceras:
                df_aux = pd.DataFrame()
                df_cabeceras: pd.Series[bool] = df["Cabecera"] == cab

                # Gauss
                try:
                    mu = df.loc[df_cambio & df_cabeceras, "AñoPromedio"].values[0]
                    sigma = df.loc[df_cambio & df_cabeceras, "desviacion_indicestandar"].values[0]
                except IndexError:
                    mu = 0
                    sigma = 0

                x = np.arange(1, 16)

                if mu != 0 and sigma != 0:
                    distribucion_normal = (norm.pdf(x, mu, sigma).round(2)) * 100
                else:
                    distribucion_normal = 0

                # print(f"Cabecera -> {cab}")
                # print(f"mu -> {df.loc[df_cambio & df_cabeceras, "AñoPromedio"].values}")
                # print(f"sigma -> {df.loc[df_cambio & df_cabeceras, "desviacion_indicestandar"].values}")
                # print(f"Distribucion normal -> {distribucion_normal}")

                # Creo el DataFrame
                df_aux["Años"] = x
                df_aux["Cambio"] = cambio
                df_aux["Cabecera"] = cab
                df_aux["Repuesto"] = self.repuesto
                df_aux["TipoRepuesto"] = self.tipo_rep
                df_aux["AñoPromedio"] = mu
                df_aux["desviacion_indicestandar"] = sigma
                df_aux["DistribucionNormal"] = distribucion_normal
                df_aux["DistribucionNormal"] = df_aux["DistribucionNormal"].fillna(0)

                df_list.append(df_aux)
        return pd.concat(df_list)


    @execute_safely
    def calcular_media_y_std_cabecera(self, df: pd.DataFrame, cambios) -> pd.DataFrame:
        for cambio in cambios:
            df_cambio = df["Cambio"] == cambio

            for cab in self.cabeceras:
                df_cabeceras = df["Cabecera"] == cab

                df.loc[df_cambio & df_cabeceras, "AñoPromedio"] = df.loc[df_cambio & df_cabeceras, "DuracionEnAños"].mean()
                df.loc[df_cambio & df_cabeceras, "desviacion_indicestandar"] = df.loc[df_cambio & df_cabeceras, "DuracionEnAños"].std(ddof=1) #std de muestreo

        df["AñoPromedio"] = df["AñoPromedio"].fillna(0).round(1)
        df["desviacion_indicestandar"] = df["desviacion_indicestandar"].fillna(0).round(1)

        return df