import streamlit as st

from config.constants_common import DEPOSITOS
from config.constants_views import PAG_REP_CODIGOS, FLOTA_CONTAINER_HEIGHT, PLACEHOLDER
from domain.entities.datos_repuestos_codigos import RepuestosCodigosFiltro

from utils.exception_utils import execute_safely
from presentation.streamlit_components import OtherComponents
from viewmodels.datos.repuestos_codigos_vm import RepuestosCodigosVM


@execute_safely
def repuestos_codigos() -> None:
    other = OtherComponents()

    st.title(PAG_REP_CODIGOS)

    aux, descrip_col, deposito_col, codigos_col, aux2 = st.columns([1, 0.65, 0.70, 0.65, 1])

    with descrip_col.container(height=FLOTA_CONTAINER_HEIGHT):
        descripcion = st.text_input("Descripción", placeholder=PLACEHOLDER, icon="📑")

    with deposito_col.container(height=FLOTA_CONTAINER_HEIGHT):
        deposito = st.multiselect("Depósito", DEPOSITOS)

    with codigos_col.container(height=FLOTA_CONTAINER_HEIGHT):
        codigos = st.text_input("Códigos", placeholder=PLACEHOLDER, icon="📦")

    df = RepuestosCodigosVM().get_df()
    df_key = "codigos_repuestos"

    if descripcion or deposito or codigos:
        repuestos_filtro = RepuestosCodigosFiltro(descripcion, deposito, codigos)
        filtros_actuales = (descripcion, deposito, codigos)

        df = RepuestosCodigosVM().get_by_args(repuestos_filtro)
        other.filter_df(df_key, filtros_actuales)

    df_paginado, paginas = other.paginate(df, 15, df_key)

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

    other.paginate_buttons(paginas, key=df_key)
