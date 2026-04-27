import base64
import io
import time

import pandas as pd
import streamlit as st

from typing import Union, Optional, Any, List

from pandas import DataFrame, Series
from streamlit.components.v1 import components
from streamlit_gsheets import GSheetsConnection

from config.constants_common import TODAY_DATE_FILE_DMY
from config.constants_views import SELECT_BOX_HEIGHT, PLACEHOLDER, CENTERED_TITLE_HEIGHT, CENTERED_TITLE_WIDTH, \
    MULTI_SELECT_BOX_HEIGHT
from config.enums import RepuestoReparadoEnum, RepuestoEnum, CabecerasEnum, TipoDuracionEnum, IndexTypeEnum, \
    ConsumoObligatorioEnum, LoadDataEnum, RoleEnum, ConsumoComparacionRepuestoEnum, PeriodoComparacionEnum
from utils.common_utils import CommonUtils


class ButtonComponents:
    def __init__(self):
        ...

    @staticmethod
    def load_data_bttn(func, key: Optional[str] = None):
        st.button(
            key=key,
            label="Cargar datos",
            type="primary",
            use_container_width=True,
            on_click=func
        )

    @staticmethod
    @st.cache_data(show_spinner=False, show_time=False)
    def _convert_to_excel(df):
        # Esta función solo corre cuando el usuario pulsa el botón
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()


    @st.fragment
    def download_df(self, df, file_name: str, col = None):
        boton = st.button("Descargar Excel 💾", type="primary", use_container_width=True)

        if boton:
            with st.spinner("Descargando archivo..."):
                excel_data = self._convert_to_excel(df)
                b64 = base64.b64encode(excel_data).decode()

                js = f"""
                    <a id="download_link" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}"></a>
                    <script>
                        setTimeout(function() {{
                            var link = document.getElementById('download_link');
                            link.click();
                            link.remove();
                        }}, 100);
                    </script>
                    """
                st.components.v1.html(js, height=0)
            st.toast("Descarga enviada al navegador", icon="📥")





class SelectBoxComponents:
    def __init__(self):
        ...

    @staticmethod
    def select_box_repuesto(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el repuesto:", RepuestoReparadoEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def select_box_tipo_repuesto(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el tipo de repuesto:", RepuestoEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def select_box_cabecera(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona la cabecera:", CabecerasEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def select_box_tipo_duracion(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el tipo de duración:", TipoDuracionEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def select_box_tipo_indice(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el tipo de índice:", IndexTypeEnum, index=0, key=key)

    @staticmethod
    def select_box_consumo_obligatorio(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el consumo obligatorio:", ConsumoObligatorioEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def select_box_load_data(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el dato a cargar:", LoadDataEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def select_box_rol(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el rol:", RoleEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def select_box_tipo_rep_comparacion(col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el tipo de repuesto:", ConsumoComparacionRepuestoEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def multi_select_box_tipo_rep_comparacion(col, key: Union[int, str]):
        with col.container(height=MULTI_SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.multiselect("Selecciona los tipos de repuestos:", ConsumoComparacionRepuestoEnum,
                                   placeholder=PLACEHOLDER, key=key)

    @staticmethod
    def multi_select_box_periodo(col, key: Union[int, str]):
        with col.container(height=MULTI_SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.multiselect("Selecciona los períodos:", PeriodoComparacionEnum,
                                  placeholder=PLACEHOLDER, key=key)


class DialogComponents:

    def __init__(self):
        ...

    @st.dialog("Error")
    def error_dialog(self, message: str):
        st.write(message)


class OtherComponents:
    def __init__(self):
        ...

    @staticmethod
    def bar_tabs(contenedor_color: str, normal_text_color: str, normal_color: str, hover_color: str,
                 active_bar_color: str, higlight_color: str):
        texto = """
                <style>
                /* Tabs container */
                .stTabs [data-baseweb="tab-list"] {{
                    background-color: {cont};
                    border-radius: 10px;
                    padding: 4px 8px;
                }}

                /* Normal tab */
                .stTabs [data-baseweb="tab"] {{
                    color: {normal_text};
                    background-color: {normal};
                    border-radius: 10px;
                    margin-right: 2px;
                    padding: 6px 8px;
                }}

                /* Hover */
                .stTabs [data-baseweb="tab"]:hover_junto {{
                    background-color: {hover};
                }}

                /* Active tab */
                .stTabs [aria-selected="true"] {{
                    background-color: {active_bar} !important;
                    color: white !important;
                }}

                /* Highlight */
                .stTabs [data-baseweb="tab-highlight"] {{
                    background-color: {highlight} !important;
                }}
                </style>
                """.format(cont=contenedor_color,
                           normal_text=normal_text_color,
                           normal=normal_color,
                           hover=hover_color,
                           active_bar=active_bar_color,
                           highlight=higlight_color)

        st.markdown(texto, unsafe_allow_html=True)


    @staticmethod
    def centered_title(col, title: str):
        with col.container(height=CENTERED_TITLE_HEIGHT, width=CENTERED_TITLE_WIDTH+250):
            st.markdown(f"<p style='text-align: center; font-size: 28px;'>{title}</p>", unsafe_allow_html=True)


    @staticmethod
    def mensaje_falta_rep(col):
        with col.container(height=SELECT_BOX_HEIGHT):
            st.text("No hay datos de este repuesto.")


    @staticmethod
    def custom_metric(col, label: str, value: Union[str, int, float], border_color: str, val_color: str,
                      delta: Optional[Union[str, int, float]] = "", delta_color: Optional[str] = ""):
        col.markdown(f"""
        <div style="
            padding:14px;
            border-radius:10px;
            border-left:5px outset {border_color};
            border-bottom:2px outset {border_color};
            background:#222;
        ">
            <div style="color:#BBB">{label}</div>
            <div style="font-size:26px; color:{val_color}">{value}</div>
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 10px;
                border-radius: 999px;
                background: rgba(76,175,80,.15);
                color: #4CAF50;
                font-weight: 600;
                font-size: 13px;
                ">{delta}</div>
        </div>
        """, unsafe_allow_html=True)


    @staticmethod
    def flash_alert_success(mensaje: str) -> None:
        placeholder = st.empty()
        placeholder.success(mensaje)
        time.sleep(2)
        placeholder.empty()


    @staticmethod
    def flash_alert_error(mensaje: str) -> None:
        placeholder = st.empty()
        placeholder.error(mensaje)
        time.sleep(2)
        placeholder.empty()


    @staticmethod
    def paginate(df: pd.DataFrame, filas_por_pagina: int, key: str) -> tuple[DataFrame, int] | tuple[Any, int] | None:
        """Pagina un dataframe y devuelve el df paginado y el total de páginas."""
        boton_descargar, aux1, aux2 = st.columns([1, 2, 2])

        with boton_descargar:
            ButtonComponents().download_df(df, f"{key.replace("_", " ")} {TODAY_DATE_FILE_DMY}.xlsx")

        df_key = f"{key}_df"
        page_key = f"{key}_page"
        mostrar_completo_toggle_key = f"{key}_ver_completos"

        mostrar_completo = st.toggle('Ver datos completos', key=mostrar_completo_toggle_key)

        if mostrar_completo:
            return df, 1

        if df_key not in st.session_state:
            st.session_state[df_key] = df

        if page_key not in st.session_state:
            st.session_state[page_key] = 0

        if st.session_state[df_key] is not None:
            # Config de la paginacion:
            total_items = len(df)
            total_paginas = max(1, (total_items + filas_por_pagina - 1) // filas_por_pagina)

            # Calcular indices
            inicio = st.session_state[page_key] * filas_por_pagina
            fin = min(inicio + filas_por_pagina, total_items)

            return df[inicio:fin], total_paginas
        return None


    @staticmethod
    def paginate_buttons(total_paginas: int, key: str):
        """Botones útiles para la paginación de dataframes"""

        if total_paginas <= 1:
            return

        page_key = f"{key}_page"
        anterior_bttn_key = f"{key}_bttn_ant"
        siguiente_bttn_key = f"{key}_bttn_sig"
        inicio_bttn_key = f"{key}_bttn_inicio"
        fin_bttn_key = f"{key}_bttn_fin"
        input_page_key = f"{key}_input_pag"
        
        disabled_ant_bttn = st.session_state[page_key] == 0
        diabled_sig_bttn = st.session_state[page_key] >= total_paginas - 1

        if input_page_key not in st.session_state:
            st.session_state[input_page_key] = st.session_state[page_key] + 1

        # Callbacks
        def ant_page():
            st.session_state[page_key] -= 1
            st.session_state[input_page_key] = st.session_state[page_key] + 1

        def sig_page():
            st.session_state[page_key] += 1
            st.session_state[input_page_key] = st.session_state[page_key] + 1

        def inicio_page():
            st.session_state[page_key] = 0
            st.session_state[input_page_key] = 1

        def fin_page():
            st.session_state[page_key] = total_paginas - 1
            st.session_state[input_page_key] = total_paginas

        def ir_a_pagina():
            st.session_state[page_key] = st.session_state[input_page_key] - 1


        ant_bttn, inicio_bttn, num_input, label, fin_bttn, siguiente_bttn = st.columns([0.25, 1.30, 0.25, 1, 0.155, 0.3],
                                                                                       vertical_alignment="bottom",
                                                                                       )

        with ant_bttn:
            st.button('← Anterior', disabled=disabled_ant_bttn, key=anterior_bttn_key, on_click=ant_page)

        with inicio_bttn:
            st.button('Inicio', key=inicio_bttn_key, on_click=inicio_page)

        with num_input:
            st.number_input("Número de página",
                min_value=1,
                max_value=total_paginas,
                step=1,
                key=input_page_key,
                on_change=ir_a_pagina,
                label_visibility="collapsed"
            )

        with label:
            st.write(f'de {total_paginas}')

        with fin_bttn:
            st.button('Fin', key=fin_bttn_key, on_click=fin_page)

        with siguiente_bttn:
            st.button('Siguiente →', disabled=diabled_sig_bttn, key=siguiente_bttn_key, width=150, on_click=sig_page)


    @staticmethod
    def filter_df(df_key: str, filtros_actuales: Any):
        prev_filter_key = f"filtros_previos_{df_key}"

        if prev_filter_key not in st.session_state or st.session_state[prev_filter_key] != filtros_actuales:
            st.session_state[f"{df_key}_page"] = 0
            st.session_state[prev_filter_key] = filtros_actuales


class GoogleSheetsComponents:
    def __init__(self, sheet_url, worksheet, cols):
        self.conn = st.connection("gsheets", type=GSheetsConnection)
        self.url = sheet_url
        self.ws = worksheet
        self.cols = cols

    def connect(self) -> pd.DataFrame:
        df_sheet = self.conn.read(spreadsheet=self.url, worksheet=self.ws, ttl=1)

        df_sheet[self.cols] = (
            df_sheet[self.cols]
            .fillna("")
            .astype(str)
            .replace(r'\.0$', '', regex=True)
        )

        df_sheet = CommonUtils().delete_unnamed_cols(df_sheet)
        return df_sheet


    def save_button(self, df_paginado, df_key, editor_key) -> None:
        if st.button("💾 Guardar cambios"):
            cambios = st.session_state.get(editor_key, {})

            if cambios.get("edited_rows") or cambios.get("added_rows") or cambios.get("deleted_rows"):
                # --- 2. FUSIONAR CAMBIOS CON EL DATAFRAME MAESTRO ---
                for idx_pantalla, modificaciones in cambios.get("edited_rows", {}).items():
                    idx_real = df_paginado.index[int(idx_pantalla)]

                    for columna, nuevo_valor in modificaciones.items():
                        st.session_state[df_key].loc[idx_real, columna] = nuevo_valor

                if cambios.get("added_rows"):
                    for fila_nueva in cambios.get("added_rows", []):
                        df_nueva = pd.DataFrame([fila_nueva])
                        st.session_state[df_key] = pd.concat([st.session_state[df_key], df_nueva],
                                                             ignore_index=True)

                if cambios.get("deleted_rows"):
                    indices_a_borrar = [df_paginado.index[int(i)] for i in cambios["deleted_rows"]]
                    st.session_state[df_key] = st.session_state[df_key].drop(indices_a_borrar)

                # --- 3. ENVIAR A GOOGLE SHEETS ---
                st.session_state[df_key] = st.session_state[df_key][
                    [col for col in self.cols if col in st.session_state[df_key].columns]
                ]

                try:
                    self.conn.update(spreadsheet=self.url, worksheet=self.ws, data=st.session_state[df_key])

                    st.toast("¡Cambios guardados en Google Sheets!", icon="💾")
                    del st.session_state[df_key]
                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.toast(f"Error al escribir en Google Sheets: {e}", icon="❌")
            else:
                st.toast("No hay cambios para guardar (Asegúrate de presionar ENTER tras editar una celda).", icon="⚠️")