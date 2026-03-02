from unittest.mock import patch

import numpy as np
import pandas as pd
from pandas._testing import assert_frame_equal

from config.enums import RepuestoEnum
from domain.services.compute_consumo_prevision import create_forecast


@patch('domain.services.compute_consumo_prevision.PrevisionDataVM') # mock de los coches
@patch('domain.services.compute_consumo_prevision.PrevisionVM') # mock del guardado
def test_calcular_indices(mock_prevision_vm, mock_data_vm):
    tipo_rep = RepuestoEnum.BURRO
    fechas_datos = pd.date_range(start='2024-01-01', end='2025-12-31', freq='MS')
    fechas_prevision = pd.date_range(start='2026-01-01', end='2026-12-31', freq='MS')

    cantidad_filas_datos = len(fechas_datos)
    cantidad_filas_prevision = len(fechas_prevision)

    df = pd.DataFrame({
        'Familia': [9] * cantidad_filas_datos,
        'Articulo': [11] * cantidad_filas_datos,
        'Codigo': ['9.00011'] * cantidad_filas_datos,
        'Repuesto': ['Burro nuevo'] * cantidad_filas_datos,
        'FechaCompleta': fechas_datos,
        'Cabecera': ['BARRACAS'] * cantidad_filas_datos,  # Mantenemos la misma cabecera para ver su evolución
        'Movimiento': ['DES'] * cantidad_filas_datos,
        'movnom': ['Salida Articulo'] * cantidad_filas_datos,
        'Cantidad': [2] * cantidad_filas_datos,
        'Interno': ['C6079'] * cantidad_filas_datos,
        'Precio': [192744.0] * cantidad_filas_datos
    })

    create_forecast(df, tipo_rep)

    mock_prevision_vm.return_value.save_df.assert_called_once()  # modk para que no se ejecute el guardado
    df_guardado_prev = mock_prevision_vm.return_value.save_df.call_args[0][0]

    df_esperado_prev = pd.DataFrame({
        'FechaCompleta': fechas_prevision.date,
        'ConsumoPrevision': [2.0] * cantidad_filas_prevision,
        'Repuesto': ['Burro nuevo'] * cantidad_filas_prevision,
        'TipoRepuesto': ['BURRO'] * cantidad_filas_prevision
    })

    mock_data_vm.return_value.save_df.assert_called_once()  # modk para que no se ejecute el guardado
    df_guardado_data = mock_data_vm.return_value.save_df.call_args[0][0]

    df_esperado_data = pd.DataFrame({
        'FechaCompleta': fechas_datos.date,
        'Consumo': np.array([2.0] * cantidad_filas_datos, dtype=np.float16),
        'Repuesto': ['Burro nuevo'] * cantidad_filas_datos,
        'TipoRepuesto': ['BURRO'] * cantidad_filas_datos
    })

    assert_frame_equal(df_guardado_prev.reset_index(drop=True), df_esperado_prev.reset_index(drop=True),
                       check_like=True)

    assert_frame_equal(df_guardado_data.reset_index(drop=True), df_esperado_data.reset_index(drop=True),
                       check_like=True)