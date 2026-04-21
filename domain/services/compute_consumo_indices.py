from typing import Optional

import numpy as np
import pandas as pd

from config.enums import IndexTypeEnum, RepuestoEnum
from utils.exception_utils import execute_safely
from viewmodels.datos.coches_cabecera_vm import CochesCabeceraVM
from viewmodels.consumo.indice.vm import IndiceConsumoVM
from domain.services.data_cleaner_listado import InventoryDataCleaner


class Index:
    def __init__(self, ) -> None:
        self.cleaner = InventoryDataCleaner()

    @execute_safely
    def calculate(self, df: pd.DataFrame, tipo_rep: RepuestoEnum, tipo_op: IndexTypeEnum, filtro: Optional[str] = None) -> None:
        if df.empty:
            print('El df está vacío.')
            return

        df['FechaCompleta'] = pd.to_datetime(df['FechaCompleta'], format="mixed", errors='coerce')
        fecha_max = df['FechaCompleta'].max()

        # Conversión de tipos optimizada
        df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')
        df['Precio'] = pd.to_numeric(df['Precio'].astype(str).str.replace(',', '.', regex=False), errors='coerce')

        df['Precio'] = df['Cantidad'] * df['Precio'] 
        
        grouped = df.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum', 'Precio':'sum'}).reset_index()

        df_mod = pd.DataFrame()
        if tipo_op == IndexTypeEnum.VEHICULO:
            df_vehicles = CochesCabeceraVM().get_df()
            df_mod = grouped.merge(df_vehicles, on='Cabecera', how='left')
            # Evitar división por cero
            df_mod['ConsumoIndice'] = np.where(df_mod['CochesDuermen'] != 0, (df_mod['Cantidad'] * 100) / df_mod['CochesDuermen'], 0)

        df_rate = df_mod.rename(columns={'Cantidad':'TotalConsumo',
                                         'Precio':'TotalCoste'})[['Cabecera', 'Repuesto', 'TotalConsumo', 'TotalCoste', 'ConsumoIndice']]

        # Modificaciones
        df_rate['TotalCoste'] = df_rate['TotalCoste'].round(0)
        df_rate['ConsumoIndice'] = df_rate['ConsumoIndice'].replace([np.inf, -np.inf], np.nan).round(1)
        df_rate['UltimaFecha'] = fecha_max.date() if pd.notna(fecha_max) else None

        df_rate.dropna(subset=['ConsumoIndice'], inplace=True)
        df_rate.insert(2, 'TipoRepuesto', tipo_rep)
        df_rate['TipoOperacion'] = tipo_op

        if filtro:
            df_rate = self.cleaner.filter(df_rate, 'Repuesto', filtro, 'startswith')

        IndiceConsumoVM().save_df(df_rate)
