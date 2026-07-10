import pandas as pd

from domain.entities.gomeria.diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from domain.entities.gomeria.transferencias_dep import GomeriaTransferenciasEntreDep
from viewmodels.base_vm import BaseVM


class TransferenciasGomeriaVM(BaseVM[GomeriaTransferenciasEntreDep]):
    def __init__(self) -> None:
        columns_df = list(GomeriaTransferenciasEntreDep.model_fields.keys())
        super().__init__(GomeriaTransferenciasEntreDep, "gomeria_transferencias", columns_df)

    def get_df_by_cabecera(self, cabecera) -> pd.DataFrame:
        return self.get_df_by_filters({"Cabecera": cabecera})


class DiferenciasGomeriaVM(BaseVM[GomeriaDiferenciaMovEntreDep]):
    def __init__(self) -> None:
        columns_df = list(GomeriaDiferenciaMovEntreDep.model_fields.keys())
        super().__init__(GomeriaDiferenciaMovEntreDep, "gomeria_diferencia_mov", columns_df)