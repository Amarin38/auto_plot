import numpy as np
import pandas as pd
from scipy.stats import norm

from src.db_data.crud_services import df_to_db
from src.utils.exception_utils import execute_safely


class DuracionRepuestos:
    def __init__(self, df: pd.DataFrame, repuesto_rep: str, tipo_duracion: str) -> None:
        self.df = df
        self.repuesto = repuesto_rep
        self.tipo_rep = tipo_duracion

    @execute_safely
    def calcular_duracion(self):
        patentes = self.df["Patente"].unique()

        for patente in patentes:
            df_separado = self.df["Patente"] == patente
            # separo por cada patende y traigo la columna Cambio, y a esa columna en ese espacio
            # le aplico el rango del tamaño de ese sub-dataframe
            self.df.loc[df_separado, "Cambio"] = range(
                len(self.df.loc[df_separado])
            )
            self.df["Repuesto"] = self.repuesto
            self.df["TipoRepuesto"] = self.tipo_rep

            # resto las fechas para saber cuanto duraron
            self.df.loc[df_separado, "DuracionEnDias"] = self.df["FechaCambio"] - self.df["FechaCambio"].shift(1)

        self.df["Cambio"] = self.df["Cambio"].astype(int)

        self.df["DuracionEnDias"] = self.df["DuracionEnDias"].dt.days.fillna(0).astype(int) # limpio de valores nulos
        self.df.loc[self.df["DuracionEnDias"] < 0, "DuracionEnDias"] = 0 # limpio de valores negativos

        self.df["DuracionEnMeses"] = round(self.df["DuracionEnDias"] / 30, 1)
        self.df["DuracionEnAños"] = round(self.df["DuracionEnDias"] / 365, 1)
        self.df["FechaCambio"] = self.df["FechaCambio"].dt.date

        self.calcular_media_y_std()

        df_to_db("duracion_repuestos", self.df)
        df_to_db("distribucion_normal", self.calcular_distribucion_normal())


    @execute_safely
    def calcular_distribucion_normal(self) -> pd.DataFrame:
        df_list = []

        for c in self.df["Cambio"].unique()[1:]:
            df_aux = pd.DataFrame()

            df_cambio = self.df["Cambio"] == c

            mu = self.df.loc[df_cambio, "AñoPromedio"].values[0]
            sigma = self.df.loc[df_cambio, "DesviacionEstandar"].values[0]
            x = np.arange(1, 13)

            df_aux["Años"] = x
            df_aux["Cambio"] = c
            df_aux["Repuesto"] = self.repuesto
            df_aux["TipoRepuesto"] = self.tipo_rep
            df_aux["AñoPromedio"] = mu
            df_aux["DesviacionEstandar"] = sigma
            df_aux["DistribucionNormal"] = norm.pdf(x, mu, sigma).round(2)
            df_aux["DistribucionNormal"] = df_aux["DistribucionNormal"] * 100

            df_list.append(df_aux)

        return pd.concat(df_list)


    @execute_safely
    def calcular_media_y_std(self) -> None:
        for c in self.df["Cambio"].unique()[1:]:
            df_cambio = self.df["Cambio"] == c

            self.df.loc[df_cambio, "AñoPromedio"] = self.df.loc[df_cambio, "DuracionEnAños"].mean().round(1)
            self.df.loc[df_cambio, "DesviacionEstandar"] = self.df.loc[df_cambio, "DuracionEnAños"].std(ddof=1).round(1) #std de muestreo

        self.df["AñoPromedio"] = self.df["AñoPromedio"].fillna(0)
        self.df["DesviacionEstandar"] = self.df["DesviacionEstandar"].fillna(0)
