from typing import Optional

import numpy as np
import pandas as pd

from config.enums import IndexTypeEnum
from utils.exception_utils import execute_safely
from viewmodels.common.coches_cabecera_vm import CochesCabeceraVM
from viewmodels.indice_consumo.vm import IndiceConsumoVM
from viewmodels.processing.data_cleaning.listado_data_cleaner import InventoryDataCleaner


class Index:
    def __init__(self, ) -> None:
        self.cleaner = InventoryDataCleaner()

    @execute_safely
    def calculate(self, df: pd.DataFrame, tipo_rep: str, tipo_op: IndexTypeEnum, filtro: Optional[str] = None) -> None:
        if not df.empty:
            df_mod = pd.DataFrame()
            fecha_max = df['FechaCompleta'].max()

            # Cambio de tipos de datos para evitar errores
            df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')
            df['Precio'] = df['Precio'].astype(str).str.replace(',','.')
            df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')


            df['Precio'] = df['Cantidad'] * df['Precio'] 
            
            grouped = df.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum', 'Precio':'sum'}).reset_index()

            match tipo_op:
                case IndexTypeEnum.VEHICULO: 
                    df_vehicles = CochesCabeceraVM().get_df()
                    df_mod = grouped.merge(df_vehicles, on='Cabecera', how='left')
                    df_mod['IndiceConsumo'] = (df_mod['Cantidad'] * 100) / df_mod['CantidadCoches']

            df_rate = df_mod.rename(columns={'Cantidad':'TotalConsumo',
                                             'Precio':'TotalCoste'})[['Cabecera', 'Repuesto', 'TotalConsumo', 'TotalCoste', 'IndiceConsumo']]

            # Modificaciones
            df_rate['TotalCoste'] = df_rate['TotalCoste'].round(0)
            df_rate['IndiceConsumo'] = df_rate['IndiceConsumo'].replace([np.inf, -np.inf], np.nan).round(1)
            df_rate['UltimaFecha'] = fecha_max
            df_rate['UltimaFecha'] = df_rate['UltimaFecha'].dt.date

            df_rate.dropna(subset=['IndiceConsumo'], inplace=True)
            df_rate.insert(2, 'TipoRepuesto', tipo_rep)
            df_rate['TipoOperacion'] = tipo_op

            if filtro is not None:
                df_rate = self.cleaner.filter(df_rate, 'Repuesto', filtro, 'startswith')

            IndiceConsumoVM().save_df(df_rate)
        else:
            print('El df está vacío.')

