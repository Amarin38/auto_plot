import pandas as pd
from unittest.mock import patch
from pandas.testing import assert_frame_equal

from domain.services.compute_consumo_indices import Index
from config.enums import IndexTypeEnum, RepuestoEnum

@patch('domain.services.compute_consumo_indices.CochesCabeceraVM') # mock de los coches
@patch('domain.services.compute_consumo_indices.IndiceConsumoVM') # mock del guardado
def test_calcular_indices(mock_indice_vm, mock_coches_cabecera):
    index_instance = Index()

    df_vehiculos_falso = pd.DataFrame({
        'Cabecera': ['BARRACAS', 'TG CALZADA', 'TG LANUS'],
        'CochesDuermen': [80, 184, 50]  # Pon los números que quieras para tu prueba
    })
    mock_coches_cabecera.return_value.get_df.return_value = df_vehiculos_falso

    df_input = pd.DataFrame({
        'Familia':[9, 9, 9, 8, "12"],
        'Articulo':[11, 72, 72, 12, "12"],
        'Codigo':['9.00011', '9.00072', '9.00072', None, "12.00012"],
        'Repuesto':['Burro nuevo', 'Burro reparado', 'Burro reparado', None, "Burro raro"],
        'FechaCompleta':['2024-10-02 00:00:00', '2024-10-05 00:00:00', '2024-10-08 00:00:00', None, '2025-10-08'],
        'Cabecera':['BARRACAS', 'TG CALZADA', 'TG CALZADA', None, "TG LANUS"],
        'Movimiento':['DES', 'DES', 'DES', None, "DES"],
        'movnom':['Salida Articulo', 'Salida Articulo', 'Salida Articulo', None, "Salida Articulo"],
        'Cantidad':[1, 1, 1, None, "10"],
        'Interno':['C6079', 'C9008', 'C2003', None, "C1999"],
        'Precio':[192744, 112224, 112224, None, "12231"]
    })

    tipo_rep = RepuestoEnum.BURRO
    tipo_op = IndexTypeEnum.VEHICULO

    index_instance.calculate(df_input, tipo_rep, tipo_op)

    mock_indice_vm.return_value.save_df.assert_called_once() # modk para que no se ejecute el guardado

    df_guardado = mock_indice_vm.return_value.save_df.call_args[0][0]

    df_esperado = pd.DataFrame({
        'Cabecera':['BARRACAS', 'TG CALZADA', 'TG LANUS'],
        'Repuesto': ['Burro nuevo', 'Burro reparado', 'Burro raro'],
        'TipoRepuesto': ['BURRO', 'BURRO', 'BURRO'],
        'TotalConsumo': [1.0, 2.0, 10.0],
        'TotalCoste': [192744.0, 224448.0, 122310.0],
        'ConsumoIndice': [1.2, 1.1, 20.0],
        'UltimaFecha': [pd.to_datetime('2025-10-08').date()] * 3,
        'TipoOperacion': ['VEHICULO', 'VEHICULO', 'VEHICULO'],
    })

    assert_frame_equal(df_guardado.reset_index(drop=True), df_esperado.reset_index(drop=True),
                       check_like=True)
