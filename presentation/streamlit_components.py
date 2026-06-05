import base64
import re
from datetime import date, datetime
import io
import time

import gspread
import pandas as pd
import streamlit as st

from typing import Union, Optional, Any, List, Tuple, Callable

from gspread import WorksheetNotFound
from pandas import DataFrame
from streamlit.components.v1 import components
from streamlit_gsheets import GSheetsConnection

from config.constants_common import TODAY_DATE_FILE_DMY, PAGE_STRFTIME_DMY, PREVISION_DF_KEY, PREVISION_DF_CONSUMO_KEY, \
    PREVISION_DF_STOCK_KEY, PREVISION_FECHAS_COLS
from config.constants_views import SELECT_BOX_HEIGHT, PLACEHOLDER, CENTERED_TITLE_HEIGHT, CENTERED_TITLE_WIDTH, \
    MULTI_SELECT_BOX_HEIGHT
from config.enums import RepuestoReparadoEnum, RepuestoEnum, CabecerasEnum, TipoDuracionEnum, IndexTypeEnum, \
    ConsumoObligatorioEnum, LoadDataEnum, RoleEnum, ConsumoComparacionRepuestoEnum, PeriodoComparacionEnum
from domain.services.compute_consumo_prevision import create_forecast_google_sheet
from utils.common_utils import CommonUtils


class ButtonComponents:
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
    def download_df(self, df, key, file_name: str, col = None):
        boton = st.button(
            "Descargar Excel 💾",
            type="primary",
            use_container_width=True,
            key=key
        )

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
                """.format(
            cont=contenedor_color,
            normal_text=normal_text_color,
            normal=normal_color,
            hover=hover_color,
            active_bar=active_bar_color,
            highlight=higlight_color
        )

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
                      delta: Optional[Union[str, int, float]] = None, delta_color: Optional[str] = ""):

        delta_html = ""

        if delta is not None and str(delta).strip() != "":
            delta_html = f"""
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
            """

        col.markdown(f"""
        <div style="
            padding:14px;
            border-radius:10px;
            border-left:5px outset {border_color};
            border-bottom:2px outset {border_color};
            background:#222;
            margin-bottom: 1.5px;
            margin-top: 1.5px;
        ">
            <div style="color:#BBB">{label}</div>
            <div style="font-size:26px; color:{val_color}">{value}</div>
            {delta_html}
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
    def filter_df(df_key: str, filtros_actuales: Any):
        prev_filter_key = f"filtros_previos_{df_key}"

        if prev_filter_key not in st.session_state or st.session_state[prev_filter_key] != filtros_actuales:
            st.session_state[f"{df_key}_page"] = 0
            st.session_state[prev_filter_key] = filtros_actuales


class Paginate:
    @staticmethod
    def create_pagination(
            df: pd.DataFrame,
            rows_per_page: int,
            key: str,
            bttn_download: bool = True
    ) -> tuple[DataFrame, int] | tuple[Any, int] | None:
        """Pagina un dataframe y devuelve el df paginado y el total de páginas."""
        boton_descargar_col, aux1, aux2 = st.columns([1, 2, 2])

        if bttn_download:
            with boton_descargar_col:
                ButtonComponents().download_df(df, key, f"{key.replace("_", " ")} {TODAY_DATE_FILE_DMY}.xlsx")

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
            total_paginas = max(1, (total_items + rows_per_page - 1) // rows_per_page)

            # Calcular indices
            inicio = st.session_state[page_key] * rows_per_page
            fin = min(inicio + rows_per_page, total_items)

            return df[inicio:fin], total_paginas
        return None


    @staticmethod
    def create_buttons(total_pages: int, key: str):
        """Botones útiles para la paginación de dataframes"""

        if total_pages <= 1:
            return

        page_key = f"{key}_page"
        anterior_bttn_key = f"{key}_bttn_ant"
        siguiente_bttn_key = f"{key}_bttn_sig"
        inicio_bttn_key = f"{key}_bttn_inicio"
        fin_bttn_key = f"{key}_bttn_fin"
        input_page_key = f"{key}_input_pag"

        disabled_ant_bttn = st.session_state[page_key] == 0
        diabled_sig_bttn = st.session_state[page_key] >= total_pages - 1

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
            st.session_state[page_key] = total_pages - 1
            st.session_state[input_page_key] = total_pages

        def ir_a_pagina():
            st.session_state[page_key] = st.session_state[input_page_key] - 1

        ant_bttn, inicio_bttn, num_input, label, fin_bttn, siguiente_bttn = st.columns(
            [0.25, 1.30, 0.25, 1, 0.155, 0.3],
            vertical_alignment="bottom",
            )

        with ant_bttn:
            st.button('← Anterior', disabled=disabled_ant_bttn, key=anterior_bttn_key, on_click=ant_page)

        with inicio_bttn:
            st.button('Inicio', key=inicio_bttn_key, on_click=inicio_page)

        with num_input:
            st.number_input("Número de página",
                            min_value=1,
                            max_value=total_pages,
                            step=1,
                            key=input_page_key,
                            on_change=ir_a_pagina,
                            label_visibility="collapsed"
                            )

        with label:
            st.write(f'de {total_pages}')

        with fin_bttn:
            st.button('Fin', key=fin_bttn_key, on_click=fin_page)

        with siguiente_bttn:
            st.button('Siguiente →', disabled=diabled_sig_bttn, key=siguiente_bttn_key, width=150, on_click=sig_page)


    @staticmethod
    def update_filters(filters_class, previous_key: str, pager_key: str):
        # Para que el paginado funcione bien una vez que filtra
        if f"filtros_anteriores_{previous_key}" not in st.session_state:
            st.session_state[f"filtros_anteriores_{previous_key}"] = vars(filters_class)

        if vars(filters_class) != st.session_state[f"filtros_anteriores_{previous_key}"]:
            # Vuelve al inicio para mostrar todos los filtros bien
            st.session_state[f"{pager_key}_page"] = 0
            st.session_state[f"{pager_key}_input_pag"] = 1

            st.session_state[f"filtros_anteriores_{previous_key}"] = vars(filters_class)


class GoogleSheetsComponents:
    def __init__(self, sheet_url, worksheet, cols):
        self.conn = st.connection("gsheets", type=GSheetsConnection)
        self.url = sheet_url
        self.ws = worksheet
        self.cols = cols

    def connect(self) -> pd.DataFrame:
        try:
            df_sheet = self.conn.read(spreadsheet=self.url, worksheet=self.ws, ttl=1)

            df_sheet[self.cols] = (
                df_sheet[self.cols]
                .fillna("")
                .astype(str)
                .replace(r'\.0$', '', regex=True)
            )

            df_sheet = CommonUtils().delete_unnamed_cols(df_sheet)
            return df_sheet
        except WorksheetNotFound:
            st.error("No existe la hoja seleccionada.")
            return pd.DataFrame(columns=self.cols)
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            return pd.DataFrame(columns=self.cols)


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


    def save_and_update_forecast(self, df_filtrado: pd.DataFrame, celda_inicio: str, col_fin: str,
                                       columnas_a_guardar: Union[List, Tuple],
                                       dynamic_editor_key: str, button_key: str) -> None:
        """
        Guarda los cambios de una tabla específica y despues recalcula
        automáticamente las previsiones usando los datos más recientes.
        """

        if st.button(f"💾 Guardar cambios", use_container_width=True, key=button_key):
            df_completo = self.update_filtered_df(dynamic_editor_key, PREVISION_DF_KEY, df_filtrado)

            df_consumo = df_completo if "Articulo" in df_completo.columns else st.session_state[PREVISION_DF_CONSUMO_KEY]
            df_stock = df_completo if "RepuestoStock" in df_completo.columns else st.session_state[PREVISION_DF_STOCK_KEY]

            for col_fecha in PREVISION_FECHAS_COLS:
                if col_fecha in df_completo.columns and col_fecha in columnas_a_guardar:
                    df_completo[col_fecha] = pd.to_datetime(df_completo[col_fecha],
                                                            format='mixed',
                                                            dayfirst=True,
                                                            errors='coerce')

                    df_completo[col_fecha] = df_completo[col_fecha].dt.to_period('M').dt.to_timestamp().dt.strftime(PAGE_STRFTIME_DMY)

            df_original = st.session_state.get(PREVISION_DF_KEY)
            hubo_cambios = False
            cambios = st.session_state.get(dynamic_editor_key, {})

            if cambios.get("edited_rows") or cambios.get("added_rows") or cambios.get("deleted_rows"):
                hubo_cambios = True
            elif df_original is not None and len(df_completo) != len(df_original):
                hubo_cambios = True

            with st.spinner("Guardando datos y recalculando pronósticos..."):
                try:
                    # --- PARTE 1: GUARDAR CAMBIOS DE LA TABLA (Si los hay) ---
                    if hubo_cambios:
                        df_recortado = df_completo[columnas_a_guardar]
                        rango_a_limpiar = f"{celda_inicio}:{col_fin}"

                        self.update_range_with_df(
                            df=df_recortado,
                            celda_inicial=celda_inicio,
                            rango_tabla=rango_a_limpiar
                        )

                        st.session_state[PREVISION_DF_KEY] = df_completo
                        st.toast("¡Tabla de datos actualizada con éxito!", icon="💾")
                    else:
                        st.toast("Calculando previsiones sin cambios manuales...", icon="ℹ️")

                    # --- PARTE 2: RECALCULAR Y GUARDAR PREVISIONES ---
                    df_prevision = create_forecast_google_sheet(df_consumo, df_stock)

                    if df_prevision is not None:
                        self.update_range_with_df(
                            df=df_prevision,
                            celda_inicial='K2',
                            rango_tabla='K2:O'
                        )
                        st.toast(f"Previsiones sincronizadas", icon="✅")
                    else:
                        st.warning("No se pudieron calcular las previsiones (revisa si hay datos suficientes).")

                    # --- PARTE 3: LIMPIEZA TOTAL Y RECARGA ---
                    st.cache_data.clear()

                    if dynamic_editor_key in st.session_state:
                        del st.session_state[dynamic_editor_key]
                    if PREVISION_DF_KEY in st.session_state:
                        del st.session_state[PREVISION_DF_KEY]

                    st.rerun()

                except Exception as e:
                    st.error(f"Error en el proceso de actualización unificado: {e}")

    def save_partial(
            self,
            df_paginado: pd.DataFrame,
            df_key: str,
            editor_key: str,
            rango: str = "A2:Z",  # ej: "B3:D2000" — define cols y fila de inicio
            date_cols: Union[List, Tuple] = (),
            date_fmt: str = "%Y-%m-%d",
            after_save: Callable | None = None,
            button_label: str = "💾 Guardar cambios",
            button_col = st,
            button_key: str | None = None,
    ) -> None:
        """
        Guarda cambios escribiendo por rango en Google Sheets.

        - Ediciones/adiciones → batch_update solo con las filas afectadas.
        - Eliminaciones       → reescritura completa del rango (inevitable).

        Params:
            rango       : Rango A1 que abarca los datos, ej. "B3:D2000".
                          La columna inicial y la fila inicial se extraen de aquí.
                          La columna final define qué columnas del DataFrame se guardan.
        """

        def _parse_rango(rango: str) -> tuple[str, int, str, int | None]:
            """'B3:D2000' → (col_ini='B', fila_ini=3, col_fin='D', fila_fin=2000)"""
            match = re.fullmatch(
                r"([A-Z]+)(\d+):([A-Z]+)(\d*)", rango.upper().replace(" ", "")
            )
            if not match:
                raise ValueError(f"Formato de rango inválido: {rango!r}  (esperado ej. 'B3:D2000')")
            col_ini, fila_ini, col_fin, fila_fin = match.groups()
            return col_ini, int(fila_ini), col_fin, int(fila_fin) if fila_fin else None

        def _col_a_num(col: str) -> int:
            """'A'→1, 'B'→2, 'AA'→27"""
            n = 0
            for ch in col.upper():
                n = n * 26 + (ord(ch) - 64)
            return n

        def _num_a_col(n: int) -> str:
            """1→'A', 27→'AA'"""
            s = ""
            while n > 0:
                n, r = divmod(n - 1, 26)
                s = chr(65 + r) + s
            return s

        def _fmt(valor, col_name: str) -> str:
            if col_name in date_cols:
                if isinstance(valor, (date, datetime, pd.Timestamp)):
                    return valor.strftime(date_fmt)
                if isinstance(valor, str) and valor:
                    try:
                        return pd.to_datetime(valor, dayfirst=True).strftime(date_fmt)
                    except Exception:
                        pass
            if pd.isna(valor) if not isinstance(valor, str) else False:
                return ""
            if isinstance(valor, float) and valor == int(valor):
                return str(int(valor))
            return str(valor)

        def _fila_a_values(df_maestro: pd.DataFrame, idx_real: int, columnas: list[str]) -> list:
            return [_fmt(df_maestro.loc[idx_real, col], col) for col in columnas]

        # ── Botón ────────────────────────────────────────────────────────────────

        kwargs = {"key": button_key} if button_key else {}
        if not button_col.button(button_label, **kwargs):
            return

        cambios = st.session_state.get(editor_key, {})
        edited = cambios.get("edited_rows", {})
        added = cambios.get("added_rows", [])
        deleted = cambios.get("deleted_rows", [])

        if not (edited or added or deleted):
            st.toast(
                "No hay cambios para guardar "
                "(Asegúrate de presionar ENTER tras editar una celda).",
                icon="⚠️",
            )

            if after_save:
                after_save(st.session_state[df_key].copy())

            st.toast(
                "Recalculando máximos y mínimos...",
                icon="🔃",
            )

            return

        # ── Parsear rango ────────────────────────────────────────────────────────

        col_ini_letra, fila_ini, col_fin_letra, _ = _parse_rango(rango)
        col_ini_num = _col_a_num(col_ini_letra)
        col_fin_num = _col_a_num(col_fin_letra)
        n_cols = col_fin_num - col_ini_num + 1  # cantidad de columnas del rango

        df_maestro: pd.DataFrame = st.session_state[df_key].copy()
        # Solo las columnas que entran en el rango definido
        columnas = df_maestro.columns.tolist()[:n_cols]

        with st.spinner("Guardando cambios..."):
            try:
                creds_dict = dict(st.secrets["connections"]["gsheets"])
                gc = gspread.service_account_from_dict(creds_dict)
                sh = gc.open_by_url(self.url)
                ws = sh.worksheet(self.ws)

                batch = []  # [{"range": "B5:D5", "values": [[v1, v2, v3]]}, ...]

                # ── 1. EDICIONES ─────────────────────────────────────────────
                if edited:
                    for idx_pantalla, modificaciones in edited.items():
                        idx_real = df_paginado.index[int(idx_pantalla)]
                        fila_sheet = fila_ini + int(idx_real)

                        # Aplicar cambio al maestro en memoria
                        for col, valor in modificaciones.items():
                            df_maestro.loc[idx_real, col] = valor

                        # Reconstruir la fila completa dentro del rango de columnas
                        values = _fila_a_values(df_maestro, idx_real, columnas)
                        rango_fila = f"{col_ini_letra}{fila_sheet}:{col_fin_letra}{fila_sheet}"
                        batch.append({"range": rango_fila, "values": [values]})

                    ws.batch_update(batch, value_input_option="USER_ENTERED")
                    batch = []

                # ── 2. ADICIONES ─────────────────────────────────────────────
                if added:
                    primer_idx = len(df_maestro)
                    nuevas = pd.DataFrame(added)
                    df_maestro = pd.concat([df_maestro, nuevas], ignore_index=True)

                    for offset in range(len(added)):
                        idx_real = primer_idx + offset
                        fila_sheet = fila_ini + idx_real
                        values = _fila_a_values(df_maestro, idx_real, columnas)
                        rango_fila = f"{col_ini_letra}{fila_sheet}:{col_fin_letra}{fila_sheet}"
                        batch.append({"range": rango_fila, "values": [values]})

                    ws.batch_update(batch, value_input_option="USER_ENTERED")

                # ── 3. ELIMINACIONES (reescritura completa del rango) ─────────
                if deleted:
                    indices_reales = [df_paginado.index[int(i)] for i in deleted]
                    df_maestro = df_maestro.drop(indices_reales).reset_index(drop=True)

                    # Formatear y construir values completos
                    df_export = df_maestro[columnas].copy()
                    for col in columnas:
                        if col in date_cols:
                            df_export[col] = df_export[col].apply(
                                lambda x: x.strftime(date_fmt)
                                if isinstance(x, (date, datetime, pd.Timestamp)) else x
                            )
                    df_export = df_export.fillna("").astype(str)
                    # Limpiar .0 residuales
                    df_export = df_export.replace(r"\.0$", "", regex=True)

                    values_data = df_export.values.tolist()

                    ws.batch_clear([rango])
                    if values_data:
                        celda_inicio = f"{col_ini_letra}{fila_ini}"
                        ws.update(
                            range_name=celda_inicio,
                            values=values_data,
                            value_input_option="USER_ENTERED",
                        )

                # ── 4. PERSISTIR Y RECARGAR ───────────────────────────────────
                st.session_state[df_key] = df_maestro
                st.toast("¡Cambios guardados en Google Sheets!", icon="💾")

                if after_save:
                    after_save(df_maestro)

                if editor_key in st.session_state:
                    del st.session_state[editor_key]
                st.cache_data.clear()
                st.rerun()

            except Exception as e:
                st.toast(f"Error al escribir en Google Sheets: {e}", icon="❌")

    def save_full(self, df: pd.DataFrame, rango: str, date_cols: list = None) -> None:
        """
        Sobrescribe un rango completo en Google Sheets con el DataFrame proporcionado.
        Ideal para guardar datos calculados por código de forma automática.
        """
        # Por defecto, asumimos que estas dos pueden venir como fecha en tu app
        if date_cols is None:
            date_cols = ["Fecha", "FechaStock"]

        with st.spinner("Guardando tabla calculada en Google Sheets..."):
            try:
                creds_dict = dict(st.secrets["connections"]["gsheets"])
                gc = gspread.service_account_from_dict(creds_dict)
                sh = gc.open_by_url(self.url)
                ws = sh.worksheet(self.ws)

                df_export = df.copy()

                for col in date_cols:
                    if col in df_export.columns:
                        df_export[col] = pd.to_datetime(df_export[col], errors='coerce')
                        df_export[col] = df_export[col].dt.strftime('%Y-%m-%d')
                        df_export[col] = df_export[col].fillna("")

                df_export = df_export.fillna("").astype(str)
                df_export = df_export.replace(r"\.0$", "", regex=True)
                df_export = df_export.replace("nan", "")
                df_export = df_export.replace("NaT", "")

                values_data = df_export.values.tolist()

                match = re.fullmatch(r"([A-Z]+)(\d+):.*", rango.upper().replace(" ", ""))
                if not match:
                    raise ValueError(f"Formato de rango inválido: {rango}")
                celda_inicio = f"{match.group(1)}{match.group(2)}"

                ws.batch_clear([rango])
                if values_data:
                    ws.update(
                        range_name=celda_inicio,
                        values=values_data,
                        value_input_option="USER_ENTERED",
                    )
                st.toast("¡Cálculos guardados correctamente!", icon="✅")

            except Exception as e:
                st.toast(f"Error al escribir los cálculos en Google Sheets: {e}", icon="❌")

    @staticmethod
    def update_filtered_df(dynamic_key: str, main_df_key: str, filtered_df: pd.DataFrame) -> pd.DataFrame:
        cambios = st.session_state[dynamic_key]
        df_completo = st.session_state[main_df_key].copy()

        indices_a_borrar = [filtered_df.index[i] for i in cambios.get("deleted_rows", [])]
        if indices_a_borrar:
            df_completo = df_completo.drop(indices_a_borrar)

        for fila_relativa, columnas in cambios.get("edited_rows", {}).items():
            idx_real = filtered_df.index[fila_relativa]
            for col, valor in columnas.items():
                df_completo.at[idx_real, col] = valor

        if cambios.get("added_rows"):
            nuevas_filas = pd.DataFrame(cambios.get("added_rows"))
            df_completo = pd.concat([df_completo, nuevas_filas], ignore_index=True)
        return df_completo

    def update_range_with_df(self, df: pd.DataFrame, celda_inicial: str,
                             rango_tabla: str, include_headers: bool = False) -> None:
        if df is None or df.empty:
            return

        df = df.copy()
        try:
            creds_dict = dict(st.secrets["connections"]["gsheets"])
            gc = gspread.service_account_from_dict(creds_dict)
            sh = gc.open_by_url(self.url)
            ws = sh.worksheet(self.ws)

            if rango_tabla:
                ws.batch_clear([rango_tabla])

            for col in df.columns:
                df[col] = df[col].apply(
                    lambda x: x.strftime('%d/%m/%Y') if isinstance(x, (date, datetime, pd.Timestamp)) else x
                )

            df = df.fillna("")

            if include_headers:
                values = [df.columns.tolist()] + df.values.tolist()
            else:
                values = df.values.tolist()

            ws.update(range_name=celda_inicial, values=values, value_input_option='USER_ENTERED')

        except Exception as e:
            st.error(f"Error genérico al escribir en Google Sheets: {e}")

