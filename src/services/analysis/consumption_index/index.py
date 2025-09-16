import pandas as pd
import numpy as np

from typing import Optional

from src.config.enums import IndexTypeEnum

from src.utils.exception_utils import execute_safely

from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner

from src.db.crud_common import db_to_df, df_to_db

class Index:
    def __init__(self, ) -> None:
        self.cleaner = InventoryDataCleaner()


    @execute_safely
    def calculate(self, df: pd.DataFrame, tipo_rep: str, tipo_op: IndexTypeEnum, filtro: Optional[str] = None) -> None:
        if not df.empty:
            fecha_max = df['FechaCompleta'].max()

            # Cambio de tipos de datos para evitar errores
            df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')
            df['Precio'] = df['Precio'].astype(str).str.replace(',','.')
            df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')


            df['Precio'] = df['Cantidad'] * df['Precio'] 
            
            grouped = df.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum', 'Precio':'sum'}).reset_index()

            match tipo_op:
                case IndexTypeEnum.VEHICLE: 
                    df_vehicles = db_to_df('coches_cabecera')
                    df_mod = grouped.merge(df_vehicles, on='Cabecera', how='left')
                case IndexTypeEnum.MOTOR: 
                    df_motors = db_to_df('motores_cabecera')
                    df_mod = grouped.merge(df_motors, on=['Cabecera', 'Repuesto'], how='right')

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

            df_to_db('index_repuesto', df_rate, 'append') # guardo el proyecto en la base de datos
        else:
            print('El df está vacío.')


    # def calculate_by_motor(self, df: pd.DataFrame, tipo: str) -> None:
    #     df_motors = self.services.db_to_df('motores_cabecera')
        
    #     if not df.empty:
    #         grouped = df.groupby(['Cabecera', 'Repuesto']).agg({'Cantidad':'sum'}).reset_index()

    #         df_with_motors = grouped.merge(df_motors, on=['Cabecera', 'Repuesto'], how='right') # hago join con la cantidad de coches para hacer el cálculo
    #         df_with_motors['IndiceConsumo'] = round((df_with_motors['Cantidad']*100) / df_with_motors['CantidadMotores'], 1) # hago el cálculo y se lo asigno a una nueva columna

    #         df_rate = df_with_motors[['Cabecera', 'Repuesto', 'IndiceConsumo']]
    #         df_rate['IndiceConsumo'].replace([np.inf, -np.inf], np.nan, inplace=True)

    #         df_rate.dropna(subset=['IndiceConsumo'], inplace=True)
    #         df_rate.insert(2, 'TipoRepuesto', tipo)
    #         df_rate['TipoOperacion'] = IndexTypeEnum.MOTOR
    #     else:
    #         print('El df está vacío.')