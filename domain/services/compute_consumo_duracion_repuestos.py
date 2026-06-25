from typing import Optional

import numpy as np
import pandas as pd
from pandas.core.arrays import ExtensionArray
from scipy.stats import norm

from utils.exception_utils import execute_safely
from viewmodels.consumo.duracion_rep.vm import DuracionRepuestosVM

class DuracionRepuestos:
    def __init__(self, df: pd.DataFrame, repuesto_rep: str, tipo_duracion: str) -> None:
        self.df         = df.copy()
        self.repuesto   = repuesto_rep
        self.tipo_rep   = tipo_duracion

        self.vm                 = DuracionRepuestosVM()
        self.cabeceras          = self.df["Cabecera"].unique()
        self.df["FechaCambio"]  = pd.to_datetime(self.df["FechaCambio"])


    @execute_safely
    def calcular_duracion(self):
        self.df = self.df.sort_values(by=["Patente", "FechaCambio"]).reset_index(drop=True)

        df_patente = self.df.groupby("Patente")

        self.df["Cambio"]               = df_patente.cumcount()
        self.df["DuracionEnDias"]       = df_patente["FechaCambio"].diff().dt.days.fillna(0).astype(int)
        self.df["DuracionEnDias"]       = np.maximum(self.df["DuracionEnDias"], 0)
        self.df["Repuesto"]             = self.repuesto
        self.df["TipoRepuesto"]         = self.tipo_rep
        self.df["DuracionEnMeses"]      = round(self.df["DuracionEnDias"] / 30, 1)
        self.df["DuracionEnAños"]       = round(self.df["DuracionEnDias"] / 365, 1)
        self.df["FechaCambio"]          = self.df["FechaCambio"].dt.date

        self.calcular_media_y_std()
        self.calcular_distribucion_normal()


    @execute_safely
    def calcular_media_y_std(self) -> None:
        df_cambio = self.df.groupby("Cambio")["DuracionEnAños"]

        self.df["AñoPromedio"] = df_cambio.transform("mean").round(1).fillna(0)
        self.df["DesviacionEstandar"] = df_cambio.transform("std").round(1).fillna(0)

        print(self.df)
        self.vm.save_df(self.df)


    @execute_safely
    def calcular_distribucion_normal(self) -> None:
        df_list     = []
        cambios     = self.df["Cambio"].unique()[1:]
        cabeceras   = self.cabeceras if self.cabeceras is not None else [None] * len(cambios)

        for cambio in cambios:
            for cabecera in cabeceras:
                if cabecera is None or pd.isna(cabecera):
                    mask = (self.df["Cambio"] == cambio)
                else:
                    mask = (self.df["Cambio"] == cambio) & (self.df["Cabecera"] == cabecera)

                df_cabecera = self.crear_df_distribucion_normal(mask, cambio, cabecera)
                df_list.append(df_cabecera)

        df_dist_normal = pd.concat(df_list)
        # df_dist_normal["Cambio"] = np.nan

        print(df_dist_normal)
        self.vm.save_distribucion_df(df_dist_normal)


    @execute_safely
    def crear_df_distribucion_normal(self, mask: bool, cambio: ExtensionArray,
                                           cabecera: Optional[ExtensionArray] = None) -> pd.DataFrame:
        df_final = pd.DataFrame()
        df_filtrado = self.df[mask]

        x = np.arange(0.5, 15.5, 0.5)

        if not df_filtrado.empty:
            mu                  = df_filtrado["AñoPromedio"].iloc[0]
            sigma               = df_filtrado["DesviacionEstandar"].iloc[0]
            distribucion_normal = (norm.pdf(x, mu, sigma).round(2)) * 100
        else:
            mu, sigma = 0, 0
            distribucion_normal = 0


        df_final["Años"]                  = x
        df_final["Cambio"]                = cambio
        if cabecera is not None:
            df_final["Cabecera"]          = cabecera
        df_final["Repuesto"]              = self.repuesto
        df_final["TipoRepuesto"]          = self.tipo_rep
        df_final["AñoPromedio"]           = mu
        df_final["DesviacionEstandar"]    = sigma
        df_final["DistribucionNormal"]    = distribucion_normal
        df_final["DistribucionNormal"]    = df_final["DistribucionNormal"].fillna(0)

        return df_final