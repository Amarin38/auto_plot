import numpy as np
import pandas as pd
import pytest
from statsmodels.compat.pandas import assert_frame_equal

from utils.common_utils import CommonUtils

utils = CommonUtils()

def test_concat_dataframes():
    df_a = pd.DataFrame({
        "Repuesto":["Bananas", "Compresores"],
        "Cabecera":["Pompeya", "TG Calzada"]
    })

    df_b = pd.DataFrame({
        "Repuesto": ["Inyectores", "Urea"],
        "Cabecera": ["La noria", "TG Lanus"]
    })

    df: pd.DataFrame = utils.concat_dataframes([df_a, df_b])

    assert len(df) == len(df_a) + len(df_b)


@pytest.mark.parametrize("valor, esperado", [
    (100, "100"),
    (10_000, "10 mil"),
    (100_000, "100 mil"),
    (1_000_000, "1 M"),
    (1_000_000_000, "1 mil M")
])
def test_abreviar_es(valor, esperado):
    assert utils.abreviar_es(valor) == esperado


@pytest.mark.parametrize("valor, esperado", [
    (1, 1),
    (1.0, 1),
    ("1", 1),
    ("1.0", 1),
    (" 1 ", 1),
    (" 1.0 ", 1),
    (" ", None),
    ("", None),
    (None, None),
    (pd.NA, None),
    (np.nan, None),
])
def test_safe_int(valor, esperado):
    assert utils.safe_int(valor) == esperado


@pytest.mark.parametrize("valor, esperado", [
    (1.0, 1.0),
    (1, 1.0),
    ("1", 1.0),
    ("1.0", 1.0),
    (" 1 ", 1.0),
    (" 1.0 ", 1.0),
    (" ", None),
    ("", None),
    (None, None),
    (pd.NA, None),
    (np.nan, None),
])
def test_safe_float(valor, esperado):
    assert utils.safe_float(valor) == esperado


@pytest.mark.parametrize("valor, esperado", [
    (1.0, None),
    (1, None),
    ("1", None),
    ("1.0", None),
    (" 1 ", None),
    (" 1.0 ", None),
    (" ", None),
    ("", None),
    (None, None),
    (pd.NA, None),
    (np.nan, None),
    ("2025-12-31", pd.to_datetime("2025-12-31").date()),
    ("2025-12-31 00:00:00", pd.to_datetime("2025-12-31").date()),
    ("2025-31-31", None),
    ("a", None)
])
def test_safe_date(valor, esperado):
    assert utils.safe_date(valor) == esperado


@pytest.mark.parametrize("valor, esperado", [
    (4_100.0045, "4.100,00"),
    ("4_100.0045", "4.100,00"),
    (" 4_100.0045 ", "4.100,00"),
    ("a", None),
    (" ", None),
    ("", None),
    (None, None),
    (pd.NA, None),
    (np.nan, None),
])
def test_num_parser(valor, esperado):
    assert utils.num_parser(valor) == esperado


def test_delete_unnamed_cols():
    df_input_unn = pd.DataFrame({
        "Repuesto": ["Bananas", "Compresores"],
        "Unnamed": [1, 2]
    })

    df_input_col = pd.DataFrame({
        "Repuesto": ["Bananas", "Compresores"],
        "Columna": [1, 2]
    })

    df_input_ambas = pd.DataFrame({
        "Repuesto": ["Bananas", "Compresores"],
        "Columna": [1, 2],
        "Unnamed": [1, 2]
    })

    df_unn = utils.delete_unnamed_cols(df_input_unn)
    df_col = utils.delete_unnamed_cols(df_input_col)
    df_ambas = utils.delete_unnamed_cols(df_input_ambas)

    df_esperado = pd.DataFrame({
        "Repuesto": ["Bananas", "Compresores"]
    })

    assert_frame_equal(df_unn.reset_index(drop=True), df_esperado.reset_index(drop=True),
                       check_like=True)

    assert_frame_equal(df_col.reset_index(drop=True), df_esperado.reset_index(drop=True),
                       check_like=True)

    assert_frame_equal(df_ambas.reset_index(drop=True), df_esperado.reset_index(drop=True),
                       check_like=True)