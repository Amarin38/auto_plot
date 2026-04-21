import streamlit as st

from config.constants_views import PAG_PROVEEDORES, FLOTA_CONTAINER_HEIGHT, PLACEHOLDER
from domain.entities.datos_proveedores import Proveedores

from utils.exception_utils import execute_safely
from presentation.streamlit_components import OtherComponents
from viewmodels.datos.proveedores_vm import ProveedoresVM


@execute_safely
def proveedores() -> None:
    other = OtherComponents()
    st.title(PAG_PROVEEDORES)

    aux, izq_col, centro_col, der_col, aux2 = st.columns([1, 0.65, 0.70, 0.65, 1])

    with izq_col.container(height=FLOTA_CONTAINER_HEIGHT):
        nro_prov = st.number_input("Número proveedor", placeholder=PLACEHOLDER, icon="🚌")

    with centro_col.container(height=FLOTA_CONTAINER_HEIGHT):
        razon_social = st.text_input("Razón Social", placeholder=PLACEHOLDER, icon="🚌")

    with der_col.container(height=FLOTA_CONTAINER_HEIGHT):
        cuit = st.text_input("CUIT", placeholder=PLACEHOLDER, icon="🚌")

    with izq_col.container(height=FLOTA_CONTAINER_HEIGHT):  # TODO: Agregas más localidades
        localidad = st.multiselect("Localidad", ["VILLA MADERO", "WILDE"])

    with centro_col.container(height=FLOTA_CONTAINER_HEIGHT):
        mail = st.text_input("Mail", placeholder=PLACEHOLDER, icon="🚌")

    with der_col.container(height=FLOTA_CONTAINER_HEIGHT):
        telefono = st.text_input("Telefono", placeholder=PLACEHOLDER, icon="🚌")


    df = ProveedoresVM().get_df()
    df_key = "datos_proveedores"

    if nro_prov or razon_social or cuit or localidad or mail or telefono:
        repuestos_filtro = Proveedores(nro_prov, razon_social, cuit, localidad, mail, telefono)
        filtros_actuales = (nro_prov, razon_social, cuit, localidad, mail, telefono)

        df = ProveedoresVM().get_by_args(repuestos_filtro)
        other.filter_df(df_key, filtros_actuales)

    df_paginado, paginas = other.paginate(df, 15, df_key)

    st.data_editor(
        df_paginado,
        disabled=True,
        hide_index=True,
        height=600,
        column_order=["NroProv", "RazonSocial", "CUIT", "Localidad", "Mail", "Telefono"],
        column_config={
            "NroProv": st.column_config.NumberColumn("Num. Proveedor", width=10),
            "RazonSocial": st.column_config.TextColumn("R. Social", width=80),
            "CUIT": st.column_config.TextColumn("CUIT", width=30),
            "Localidad": st.column_config.TextColumn("Localidad", width=50),
            "Mail": st.column_config.TextColumn("Mail", width=30),
            "Telefono": st.column_config.TextColumn("Telefono", width=30),
        }
    )

    other.paginate_buttons(paginas, key=df_key)
