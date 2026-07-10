import numpy as np
import streamlit as st

from config.constants_common import LOC_PROVEEDORES, PROVEEDORES_SHEET_URL, PROVEEDORES_WS, PROVEEDORES_COLS, INDEX, \
    PROVEEDORES_DF_KEY, PROVEEDORES_PAGER_KEY, PROVEEDORES_EDITOR_KEY
from config.constants_views import PAG_PROVEEDORES, FLOTA_CONTAINER_HEIGHT, PLACEHOLDER

from utils.exception_utils import execute_safely
from presentation.streamlit_components import OtherComponents, GoogleSheetsComponents, Paginate


class Filtros:
    pass

google_sheet = GoogleSheetsComponents(PROVEEDORES_SHEET_URL, PROVEEDORES_WS, PROVEEDORES_COLS)

@st.cache_data(ttl=200, show_spinner=True)
def get_sheet():
    return google_sheet.connect()

@execute_safely
def proveedores() -> None:
    paginate = Paginate()
    filtros = Filtros()


    st.title(PAG_PROVEEDORES)

    _, izq_col, centro_col, der_col, _ = st.columns([1, 0.65, 0.70, 0.65, 1])

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


    filtros.nro_prov = nro_prov
    filtros.razon_social = razon_social
    filtros.cuit = cuit
    filtros.localidad = localidad
    filtros.mail = mail
    filtros.telefono = telefono

    if PROVEEDORES_DF_KEY not in st.session_state:
        st.session_state[PROVEEDORES_DF_KEY] = df_sheet

    df_prov = st.session_state[PROVEEDORES_DF_KEY]
    mask = filtros_proveedores(df_prov, filtros)
    paginate.update_filters(filtros, "proveedores", PROVEEDORES_PAGER_KEY)

    # -----------------------------------------------------------------------------------------------
    df_paginado, paginas = paginate.create_pagination(df_prov[mask], 15, PROVEEDORES_PAGER_KEY)
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
            "NroProv"       : st.column_config.NumberColumn("Num. Proveedor", width=1),
            "RazonSocial"   : st.column_config.TextColumn("R. Social", width=150),
            "CUIT"          : st.column_config.TextColumn("CUIT", width=10),
            "Localidad"     : st.column_config.TextColumn("Localidad", width=60),
            "Mail"          : st.column_config.TextColumn("Mail", width=60),
            "Telefono"      : st.column_config.TextColumn("Telefono", width=10),
        }
    )

    google_sheet.save_button(df_paginado, df_key=PROVEEDORES_DF_KEY, editor_key=PROVEEDORES_EDITOR_KEY)
    paginate.create_buttons(paginas, key=PROVEEDORES_PAGER_KEY)


def filtros_proveedores(df, filtros):
    mask = np.ones(len(df), dtype=bool)

    if filtros.nro_prov:
        mask &= df["NroProv"] == filtros.nro_prov

    if filtros.razon_social:
        mask &= df["RazonSocial"].str.startswith(filtros.razon_social.strip().upper())

    if filtros.cuit:
        mask &= df["CUIT"].str.startswith(filtros.cuit.strip())

    if filtros.localidad:
        mask &= df["Localidad"].isin(filtros.localidad)

    if filtros.mail:
        mask &= df["Mail"].str.contains(filtros.mail.strip())

    if filtros.telefono:
        mask &= df["Telefono"].str.contains(filtros.telefono.strip())

    return mask