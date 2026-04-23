import pandas as pd
import streamlit as st

from config.constants_common import LOC_PROVEEDORES, PROVEEDORES_SHEET_URL, PROVEEDORES_COLS, PROVEEDORES_WS
from config.constants_views import PAG_PROVEEDORES, FLOTA_CONTAINER_HEIGHT, PLACEHOLDER
from domain.entities.datos_proveedores import Proveedores
from utils.common_utils import CommonUtils

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

    df_sheet = other.google_sheet_conn(
        sheet_url=PROVEEDORES_SHEET_URL,
        worksheet=PROVEEDORES_WS,
        cols=PROVEEDORES_COLS
    )
    df_sheet = CommonUtils().delete_unnamed_cols(df_sheet)

    if "_index" in df_sheet.columns:
        df_sheet = df_sheet.drop(columns=["_index"])

    if "df_proveedores" not in st.session_state:
        st.session_state.df_proveedores = df_sheet

        vm.backup_google_sheet(
            df_viejo=vm.get_df(),
            df_nuevo=st.session_state.df_proveedores
        )
        st.toast("Backup sincronizado correctamente.", icon="🔄")
        st.rerun()

    df_key = "datos_proveedores"

    if nro_prov or razon_social or cuit or localidad or mail or telefono:
        repuestos_filtro = Proveedores(nro_prov, razon_social, cuit, localidad, mail, telefono)
        filtros_actuales = (nro_prov, razon_social, cuit, tuple(localidad), mail, telefono)

        st.session_state.df_proveedores = vm.get_by_args(repuestos_filtro)
        other.filter_df(df_key, filtros_actuales)
    else:
        st.session_state.df_proveedores = df_sheet

    df_paginado, paginas = other.paginate(st.session_state.df_proveedores, 15, df_key)

    df_visual = df_paginado.reset_index(drop=True)
    st.data_editor(
        df_visual,
        disabled=False,
        num_rows="dynamic",
        hide_index=True,
        height=600,
        key="editor_proveedores",
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

    if st.button("💾 Guardar cambios"):
        cambios = st.session_state.get("editor_proveedores", {})

        if cambios.get("edited_rows") or cambios.get("added_rows") or cambios.get("deleted_rows"):
            # --- 2. FUSIONAR CAMBIOS CON EL DATAFRAME MAESTRO ---
            for idx_pantalla, modificaciones in cambios.get("edited_rows", {}).items():
                idx_real = df_paginado.index[int(idx_pantalla)]

                for columna, nuevo_valor in modificaciones.items():
                    st.session_state.df_proveedores.loc[idx_real, columna] = nuevo_valor


            if cambios.get("added_rows"):
                # try:
                #     ultimo_id = int(pd.to_numeric(st.session_state.df_proveedores["NroProv"]).max())
                # except:
                #     ultimo_id = 0

                for fila_nueva in cambios.get("added_rows", []):
                    # ultimo_id += 1
                    # fila_nueva["NroProv"] = ultimo_id

                    df_nueva = pd.DataFrame([fila_nueva])
                    st.session_state.df_proveedores = pd.concat([st.session_state.df_proveedores, df_nueva],
                                                                ignore_index=True)

            if cambios.get("deleted_rows"):
                indices_a_borrar = [df_paginado.index[int(i)] for i in cambios["deleted_rows"]]
                st.session_state.df_proveedores = st.session_state.df_proveedores.drop(indices_a_borrar)

            # --- 3. ENVIAR A GOOGLE SHEETS ---
            st.session_state.df_proveedores = st.session_state.df_proveedores[
                [col for col in PROVEEDORES_COLS if col in st.session_state.df_proveedores.columns]
            ]

            try:
                other.update_google_sheet(
                    sheet_url=PROVEEDORES_SHEET_URL,
                    worksheet=PROVEEDORES_WS,
                    data=st.session_state.df_proveedores
                )

                st.toast("¡Cambios guardados en Google Sheets!", icon="💾")
                del st.session_state["df_proveedores"]
                st.cache_data.clear()
                st.rerun()

            except Exception as e:
                st.toast(f"Error al escribir en Google Sheets: {e}", icon="❌")
        else:
            st.toast("No hay cambios para guardar (Asegúrate de presionar ENTER tras editar una celda).", icon="⚠️")

    other.paginate_buttons(paginas, key=df_key)
