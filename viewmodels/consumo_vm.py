from typing import List

import pandas as pd

from config.enums import CabecerasEnum, ConsumoComparacionRepuestoEnum, PeriodoComparacionEnum, ConsumoObligatorioEnum
from domain.entities.consumo.comparacion import ConsumoComparacion
from domain.entities.consumo.desviacion_indices import ConsumoDesviacionIndices
from domain.entities.consumo.distribucion_normal import DistribucionNormal
from domain.entities.consumo.duracion_repuestos import DuracionRepuestos
from domain.entities.consumo.historial import ConsumoHistorial
from domain.entities.consumo.indice import ConsumoIndice
from domain.entities.consumo.obligatorio import ConsumoObligatorio
from domain.entities.consumo.prevision import ConsumoPrevision
from domain.entities.consumo.prevision_data import ConsumoPrevisionData
from domain.entities.inicio_conteo_stock import ConteoStock
from viewmodels.base_vm import BaseVM


class ConsumoComparacionVM(BaseVM[ConsumoComparacion]):
    def __init__(self) -> None:
        columns_df = list(ConsumoComparacion.model_fields.keys())
        super().__init__(ConsumoComparacion, "consumo_comparacion", columns_df)

    def get_df_cabecera_and_tipo_rep_and_periodo(self, cabecera: CabecerasEnum,
                                                 tipo_repuesto: List[ConsumoComparacionRepuestoEnum],
                                                 periodo: List[PeriodoComparacionEnum]) -> pd.DataFrame:
        return self.get_df_by_filters({"Cabecera": cabecera, "TipoRepuesto": tipo_repuesto, "PeriodoID": periodo})


class ConsumoDuracionRepuestosVM(BaseVM[DuracionRepuestos]):
    def __init__(self) -> None:
        columns_df = list(DuracionRepuestos.model_fields.keys())
        super().__init__(DuracionRepuestos, "duracion_repuestos", columns_df)


    def get_df_by_repuesto(self, repuesto):
        return self.get_df_by_filters({"Repuesto": repuesto})


    def get_distinct_repuestos(self):
        return self.get_distinct("Repuesto")


class ConsumoDistribucionNormalDuracionVM(BaseVM[DistribucionNormal]):
    def __init__(self) -> None:
        columns_df = list(DistribucionNormal.model_fields.keys())
        super().__init__(DistribucionNormal, "distribucion_normal", columns_df)

    def get_df_by_repuesto(self, repuesto):
        return self.get_df_by_filters({"Repuesto": repuesto})


class ConteoStockVM(BaseVM[ConteoStock]):
    def __init__(self) -> None:
        columns_df = list(ConteoStock.model_fields.keys())
        super().__init__(ConteoStock, "conteo_stock", columns_df)


    def calcular_datos(self) -> dict:
        df = self.get_df()[["Recuento", "DiferenciaPrecio", "PrecioAnterior", "PrecioActual"]]

        df["DiferenciaPrecio"]  = df["DiferenciaPrecio"].to_numpy()
        df["PrecioAnterior"]    = df["PrecioAnterior"].to_numpy()
        df["PrecioActual"]      = df["PrecioActual"].to_numpy()


        precio_faltante = df.loc[df["DiferenciaPrecio"] < 0, "DiferenciaPrecio"].sum()
        precio_sobrante = df.loc[df["DiferenciaPrecio"] > 0, "DiferenciaPrecio"].sum()
        precio_anterior = df["PrecioAnterior"].sum()
        precio_actual   = df["PrecioActual"].sum()
        porcentaje_dif  = round(self.calcular_porcentaje(precio_actual, precio_anterior) - 100, 2)

        contados = df["Recuento"].notnull().sum()

        datos = {
            "precio_faltante": precio_faltante,
            "precio_sobrante": precio_sobrante,
            "precio_anterior": precio_anterior,
            "precio_actual": precio_actual,
            "porcentaje_dif": porcentaje_dif,
            "contados":contados
        }

        return datos


    @staticmethod
    def calcular_porcentaje(total: float, parte: float) -> float:
        return round((parte * 100) / total, 2)


    @staticmethod
    def calcular_porcentaje_error(a, b, c) -> float:
        return round(((-a - b) * 100) / c, 2) if c != 0 else 0


class ConsumoHistorialVM(BaseVM[ConsumoHistorial]):
    def __init__(self) -> None:
        columns_df = list(ConsumoHistorial.model_fields.keys())
        super().__init__(ConsumoHistorial, "consumo_historial", columns_df)


    def get_df_tipo_repuesto(self, tipo_repuesto):
        return self.get_df_by_filters({"TipoRepuesto": tipo_repuesto})


class ConsumoIndiceVM(BaseVM[ConsumoIndice]):
    def __init__(self) -> None:
        columns_df = list(ConsumoIndice.model_fields.keys())
        super().__init__(ConsumoIndice, "consumo_indice", columns_df)


    def get_df_tipo_repuesto_and_tipo_operacion(self, tipo_repuesto, tipo_operacion):
        return self.get_df_by_filters({"TipoRepuesto":tipo_repuesto, "TipoOperacion":tipo_operacion})


class ConsumoDesviacionIndicesVM(BaseVM[ConsumoDesviacionIndices]):
    def __init__(self) -> None:
        columns_df = list(ConsumoDesviacionIndices.model_fields.keys())
        super().__init__(ConsumoDesviacionIndices, "consumo_desviacion_indices", columns_df)


    def get_df_by_tipo_rep(self, tipo_rep):
        return self.get_df_by_filters({"TipoRepuesto": tipo_rep})


class ConsumoObligatorioVM(BaseVM[ConsumoObligatorio]):
    def __init__(self) -> None:
        columns_df = list(ConsumoObligatorio.model_fields.keys())
        super().__init__(ConsumoObligatorio, "consumo_obligatorio", columns_df)


    def get_df_by_repuesto(self, repuesto: ConsumoObligatorioEnum) -> pd.DataFrame:
        return self.get_df_by_filters({"Repuesto": repuesto})


class ConsumoPrevisionVM(BaseVM[ConsumoPrevision]):
    def __init__(self) -> None:
        columns_df = list(ConsumoPrevision.model_fields.keys())
        super().__init__(ConsumoPrevision, "consumo_prevision", columns_df)

    def get_df_by_tipo_repuesto(self, tipo_repuesto: str) -> pd.DataFrame:
        return self.get_df_by_filters({"TipoRepuesto": tipo_repuesto})


class ConsumoPrevisionDataVM(BaseVM[ConsumoPrevisionData]):
    def __init__(self) -> None:
        columns_df = list(ConsumoPrevisionData.model_fields.keys())
        super().__init__(ConsumoPrevisionData, "consumo_prevision_data", columns_df)

    def get_df_by_tipo_repuesto(self, tipo_repuesto: str) -> pd.DataFrame:
        return self.get_df_by_filters({"TipoRepuesto": tipo_repuesto})