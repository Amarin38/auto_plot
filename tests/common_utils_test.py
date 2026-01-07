import pandas as pd
import pytest
from utils.common_utils import CommonUtils



def test_concat_dataframes():
    df_a = pd.DataFrame({
        "Repuesto":["Bananas", "Compresores"],
        "Cabecera":["Pompeya", "TG Calzada"]
    })

    df_b = pd.DataFrame({
        "Repuesto": ["Inyectores", "Urea"],
        "Cabecera": ["La noria", "TG Lanus"]
    })

    df: pd.DataFrame = CommonUtils().concat_dataframes([df_a, df_b])

    assert len(df) == len(df_a) + len(df_b)



@pytest.mark.parametrize("valor, esperado", [
    (100, "100"),
    (10_000, "10 mil"),
    (100_000, "100 mil"),
    (1_000_000, "1 M"),
    (1_000_000_000, "1 mil M")
])
def test_abreviar_es(valor, esperado):
    assert CommonUtils().abreviar_es(valor) == esperado