import streamlit as st

from config.constants_common import LOC_PROVEEDORES
from config.constants_views import PAG_PROVEEDORES, FLOTA_CONTAINER_HEIGHT, PLACEHOLDER
from domain.entities.datos_proveedores import Proveedores

from utils.exception_utils import execute_safely
from presentation.streamlit_components import OtherComponents
from viewmodels.datos.proveedores_vm import ProveedoresVM


@execute_safely
def proveedores() -> None:
    other = OtherComponents()
    vm = ProveedoresVM()
    st.title(PAG_PROVEEDORES)

    aux, izq_col, centro_col, der_col, aux2 = st.columns([1, 0.65, 0.70, 0.65, 1])

    with izq_col.container(height=FLOTA_CONTAINER_HEIGHT):
        nro_prov = st.text_input("Número proveedor", placeholder=PLACEHOLDER, icon="👤")

    with centro_col.container(height=FLOTA_CONTAINER_HEIGHT):
        razon_social = st.text_input("Razón Social", placeholder=PLACEHOLDER, icon="🪪")

    with der_col.container(height=FLOTA_CONTAINER_HEIGHT):
        cuit = st.text_input("CUIT", placeholder=PLACEHOLDER, icon="📑")

    with izq_col.container(height=FLOTA_CONTAINER_HEIGHT):
        localidad = st.multiselect("Localidad", LOC_PROVEEDORES)

    with centro_col.container(height=FLOTA_CONTAINER_HEIGHT):
        mail = st.text_input("Mail", placeholder=PLACEHOLDER, icon="✉️")

    with der_col.container(height=FLOTA_CONTAINER_HEIGHT):
        telefono = st.text_input("Telefono", placeholder=PLACEHOLDER, icon="📞")


    if "df_proveedores" not in st.session_state:
        st.session_state.df_proveedores = vm.get_df()

    df_key = "datos_proveedores"

    if nro_prov or razon_social or cuit or localidad or mail or telefono:
        repuestos_filtro = Proveedores(nro_prov, razon_social, cuit, localidad, mail, telefono)
        filtros_actuales = (nro_prov, razon_social, cuit, tuple(localidad), mail, telefono)

        st.session_state.df_proveedores = vm.get_by_args(repuestos_filtro)

        other.filter_df(df_key, filtros_actuales)
    else:
        st.session_state.df_proveedores = vm.get_df()

    df_paginado, paginas = other.paginate(st.session_state.df_proveedores, 15, df_key)

    st.data_editor(
        df_paginado,
        disabled=False,
        hide_index=True,
        height=600,
        key="editor_proveedores",
        column_order=["NroProv", "RazonSocial", "CUIT", "Localidad", "Mail", "Telefono"],
        column_config={
            "NroProv": st.column_config.NumberColumn("Num. Proveedor", width=1),
            "RazonSocial": st.column_config.TextColumn("R. Social", width=150),
            "CUIT": st.column_config.TextColumn("CUIT", width=10),
            "Localidad": st.column_config.TextColumn("Localidad", width=60),
            "Mail": st.column_config.TextColumn("Mail", width=60),
            "Telefono": st.column_config.TextColumn("Telefono", width=10),
        }
    )

    if st.button("💾 Guardar cambios"):
        changes = st.session_state.get("editor_proveedores", {})
        vm.save_changes(st.session_state.df_proveedores, changes)

        # Refrescar
        del st.session_state["df_proveedores"]
        st.cache_data.clear()
        st.success("Cambios guardados!")
        st.rerun()

    other.paginate_buttons(paginas, key=df_key)
