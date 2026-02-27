import pandas as pd
from pandas import DataFrame

from domain.entities.conteo_stock import ConteoStock
from infrastructure.repositories.conteo_stock_repository import ConteoStockRepository
from utils.common_utils import CommonUtils


def calcular_contados(df: pd.DataFrame) -> int:
    return df["Recuento"].notnull().sum()


def calcular_porcentaje(total: float, parte: float) -> float:
    return round((parte * 100) / total,2)

class ConteoStockVM:
    def __init__(self) -> None:
        self.repo = ConteoStockRepository()
        self.common = CommonUtils()

    def save_df(self, df) -> None:
        entities = []

        for _, row in df.iterrows():
            entity = ConteoStock(
                id                  = None,
                Codigo              = row["Codigo"],
                Articulo            = row["Articulo"],
                Sistema             = self.common.safe_int(row["Sistema"]),
                Recuento            = self.common.safe_int(row["Recuento"]),
                Resultado           = row["Resultado"],
                Fecha               = self.common.safe_date(row["Fecha"]),
                Reconteos           = self.common.safe_float(row["Reconteos"]),
                Estanteria          = row["Estanteria"],
                Precio              = self.common.safe_float(row["Precio"]),
                DiferenciaStock     = self.common.safe_float(row["DiferenciaStock"]),
                DiferenciaPrecio    = self.common.safe_float(row["DiferenciaPrecio"]),
                PrecioAnterior      = self.common.safe_float(row["PrecioAnterior"]),
                PrecioActual        = self.common.safe_float(row["PrecioActual"]),
                Alerta              = row["Alerta"],
                Deposito            = row["Deposito"],
                Ajuste              = self.common.safe_float(row["Ajuste"]),
                StockNuevo          = self.common.safe_float(row["StockNuevo"]),
            )
            entities.append(entity)

        self.repo.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()
        return self.get_data(entities)

    def calcular_datos(self) -> tuple:
        df = self.get_df()[["Recuento", "DiferenciaPrecio", "PrecioAnterior", "PrecioActual"]]

        df["DiferenciaPrecio"]  = df["DiferenciaPrecio"].to_numpy()
        df["PrecioAnterior"]    = df["PrecioAnterior"].to_numpy()
        df["PrecioActual"]      = df["PrecioActual"].to_numpy()


        precio_faltante = df.loc[df["DiferenciaPrecio"] < 0, "DiferenciaPrecio"].sum().round(1)
        precio_sobrante = df.loc[df["DiferenciaPrecio"] > 0, "DiferenciaPrecio"].sum().round(1)
        precio_anterior = df["PrecioAnterior"].sum().round(1)
        precio_actual   = df["PrecioActual"].sum().round(1)
        porcentaje_dif  = round(calcular_porcentaje(precio_actual, precio_anterior) - 100, 2)

        return precio_faltante, precio_sobrante, precio_anterior, precio_actual, porcentaje_dif, calcular_contados(df)


    @staticmethod
    def get_data(entities) -> DataFrame:
        return pd.DataFrame([
                 {
                    "id": e.id,
                    "Codigo": e.Codigo,
                    "Articulo": e.Articulo,
                    "Sistema": e.Sistema,
                    "Recuento": e.Recuento,
                    "Resultado": e.Resultado,
                    "Fecha": e.Fecha,
                    "Reconteos": e.Reconteos,
                    "Estanteria": e.Estanteria,
                    "Precio": e.Precio,
                    "DiferenciaStock": e.DiferenciaStock,
                    "DiferenciaPrecio": e.DiferenciaPrecio,
                    "PrecioAnterior": e.PrecioAnterior,
                    "PrecioActual": e.PrecioActual,
                    "Alerta": e.Alerta,
                    "Deposito": e.Deposito,
                    "Ajuste": e.Ajuste,
                    "StockNuevo": e.StockNuevo,
                }
                for e in entities
            ])
