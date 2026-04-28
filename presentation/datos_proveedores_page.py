import streamlit as st

from config.constants_common import LOC_PROVEEDORES
from config.constants_views import PAG_PROVEEDORES, FLOTA_CONTAINER_HEIGHT, PLACEHOLDER, PROVEEDORES_DF_KEY, \
    PROVEEDORES_PAGER_KEY, PROVEEDORES_EDITOR_KEY, PROVEEDORES_SHEET_URL, PROVEEDORES_COLS, PROVEEDORES_WS, INDEX
from domain.entities.datos_proveedores import Proveedores

from utils.exception_utils import execute_safely
from presentation.streamlit_components import OtherComponents, GoogleSheetsComponents
from viewmodels.datos.proveedores_vm import ProveedoresVM


google_sheet = GoogleSheetsComponents(PROVEEDORES_SHEET_URL, PROVEEDORES_WS, PROVEEDORES_COLS)

@st.cache_data(ttl=200, show_spinner=True)
def get_sheet():
    return google_sheet.connect()

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

    df_sheet = get_sheet()

    if INDEX in df_sheet.columns:
        df_sheet = df_sheet.drop(columns=[INDEX])

    if PROVEEDORES_DF_KEY not in st.session_state:
        st.session_state[PROVEEDORES_DF_KEY] = df_sheet

        vm.backup_google_sheet( # cada vez que se recarga la página se hace un backup en google sheets
            df_viejo=vm.get_df(),
            df_nuevo=st.session_state[PROVEEDORES_DF_KEY]
        )
        st.toast("Backup sincronizado correctamente.", icon="🔄")
        st.rerun()

    # FILTROS
    if nro_prov or razon_social or cuit or localidad or mail or telefono:
        repuestos_filtro = Proveedores(nro_prov, razon_social, cuit, localidad, mail, telefono)
        filtros_actuales = (nro_prov, razon_social, cuit, tuple(localidad), mail, telefono)

        st.session_state[PROVEEDORES_DF_KEY] = vm.get_by_args(repuestos_filtro)
        other.filter_df(PROVEEDORES_PAGER_KEY, filtros_actuales)
    else:
        st.session_state[PROVEEDORES_DF_KEY] = df_sheet

    df_paginado, paginas = other.paginate(st.session_state[PROVEEDORES_DF_KEY], 15, PROVEEDORES_PAGER_KEY)

    df_visual = df_paginado.reset_index(drop=True)
    st.data_editor(
        df_visual,
        disabled=False,
        num_rows="dynamic",
        hide_index=True,
        height=600,
        key=PROVEEDORES_EDITOR_KEY,
        column_order=PROVEEDORES_COLS,
        column_config={
            "NroProv": st.column_config.NumberColumn("Num. Proveedor", width=1),
            "RazonSocial": st.column_config.TextColumn("R. Social", width=150),
            "CUIT": st.column_config.TextColumn("CUIT", width=10),
            "Localidad": st.column_config.TextColumn("Localidad", width=60),
            "Mail": st.column_config.TextColumn("Mail", width=60),
            "Telefono": st.column_config.TextColumn("Telefono", width=10),
        }
    )

    google_sheet.save_button(df_paginado, df_key=PROVEEDORES_DF_KEY, editor_key=PROVEEDORES_EDITOR_KEY)
    other.paginate_buttons(paginas, key=PROVEEDORES_PAGER_KEY)
