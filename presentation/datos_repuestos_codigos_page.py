import numpy as np
import streamlit as st

from config.constants_common import DEPOSITOS, REPUESTOS_CODIGOS_PAGER_KEY
from config.constants_views import PAG_REP_CODIGOS, FLOTA_CONTAINER_HEIGHT, PLACEHOLDER
from domain.entities.datos_repuestos_codigos import RepuestosCodigosFiltro

from utils.exception_utils import execute_safely
from presentation.streamlit_components import Paginate
from viewmodels.datos.repuestos_codigos_vm import RepuestosCodigosVM

class Filtros:
    pass


@st.cache_data(ttl=200, show_spinner=True)
def get_df():
    return RepuestosCodigosVM().get_df()


@st.cache_data(ttl=200, show_spinner=True)
def get_df_filtro(repuestos_filtro: RepuestosCodigosFiltro):
    return RepuestosCodigosVM().get_by_args(repuestos_filtro)


@execute_safely
def repuestos_codigos() -> None:
    paginate = Paginate()
    filtros = Filtros()

    st.title(PAG_REP_CODIGOS)

    _, descrip_col, deposito_col, codigos_col, _ = st.columns([1, 0.65, 0.70, 0.65, 1])

    with descrip_col.container(height=FLOTA_CONTAINER_HEIGHT):
        descripcion = st.text_input("Descripción", placeholder=PLACEHOLDER, icon="📑")

    with deposito_col.container(height=FLOTA_CONTAINER_HEIGHT):
        deposito = st.multiselect("Depósito", DEPOSITOS)

    with codigos_col.container(height=FLOTA_CONTAINER_HEIGHT):
        codigos = st.text_input("Códigos", placeholder=PLACEHOLDER, icon="📦")

    filtros.descripcion = descripcion
    filtros.deposito = deposito
    filtros.codigos = codigos

    df = get_df()

    mask = np.ones(len(df), dtype=bool)

    if filtros.descripcion:
        mask &= (
            df["Descripcion"]
                .str.upper()
                .str.startswith(str(filtros.descripcion.strip().upper()), na=False)
        )

    if filtros.deposito:
        mask &= (
            df["Deposito"]
                .astype(str)
                .str.strip()
                .str.upper()
                .isin(filtros.deposito)
        )

    if filtros.codigos:
        mask &= (
            df["CodigosConCero"]
                .str.replace(r'\.0$', '', regex=True)
                .str.strip()
                .str.startswith(str(filtros.codigos.strip()), na=False)
        )

    df = df[mask]

    paginate.update_filters(filtros, "codigos_repuestos", REPUESTOS_CODIGOS_PAGER_KEY)

    df_paginado, paginas = paginate.create_pagination(df, 15, REPUESTOS_CODIGOS_PAGER_KEY)

    st.data_editor(
        df_paginado,
        disabled=True,
        hide_index=True,
        height=600,
        column_order=["Descripcion", "Deposito", "CodigosConCero"],
        column_config={
            "Descripcion": st.column_config.TextColumn("Descripción", width=450),
            "Deposito": st.column_config.TextColumn("Depósito", width=1),
            "CodigosConCero": st.column_config.TextColumn("Códigos", width=1),
        }
    )

    paginate.create_buttons(paginas, key=REPUESTOS_CODIGOS_PAGER_KEY)
