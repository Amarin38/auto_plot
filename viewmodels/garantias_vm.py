import dataclasses

import pandas as pd

from domain.entities.garantias.consumo import GarantiasConsumo
from domain.entities.garantias.datos import GarantiasDatos
from domain.entities.garantias.falla import GarantiasFalla
from viewmodels.base_vm import BaseVM


class FallaGarantiasVM(BaseVM[GarantiasFalla]):
    def __init__(self) -> None:
        columns_df = list(GarantiasFalla.model_fields.keys())
        super().__init__(GarantiasFalla, "garantias_falla", columns_df)
    
    def get_df_by_tipo_and_cabecera(self, tipo_repuesto, cabecera) -> pd.DataFrame:
        return self.get_df_by_filters({"TipoRepuesto": tipo_repuesto, "Cabecera": cabecera})


class DatosGarantiasVM(BaseVM[GarantiasDatos]):
    def __init__(self) -> None:
        columns_df = list(GarantiasDatos.model_fields.keys())
        super().__init__(GarantiasDatos, "garantias_datos", columns_df)


class ConsumoGarantiasVM(BaseVM[GarantiasConsumo]):
    def __init__(self) -> None:
        columns_df = list(GarantiasConsumo.model_fields.keys())
        super().__init__(GarantiasConsumo, "garantias_consumo", columns_df)
    
    def get_df_by_tipo_and_cabecera(self, tipo_repuesto, cabecera) -> pd.DataFrame:
        return self.get_df_by_filters({"TipoRepuesto": tipo_repuesto, "Cabecera": cabecera})
