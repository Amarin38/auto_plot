import time

import streamlit as st

from utils.exception_utils import execute_safely

from typing import Union, Optional

from config.constants_views import SELECT_BOX_HEIGHT, PLACEHOLDER, CENTERED_TITLE_HEIGHT, CENTERED_TITLE_WIDTH, \
    MULTI_SELECT_BOX_HEIGHT
from config.enums import RepuestoReparadoEnum, RepuestoEnum, CabecerasEnum, TipoDuracionEnum, IndexTypeEnum, \
    ConsumoObligatorioEnum, LoadDataEnum, RoleEnum, ConsumoComparacionRepuestoEnum, PeriodoComparacionEnum


class ButtonComponents:
    def __init__(self):
        ...

    @execute_safely
    def load_data_bttn(self, func, key: Optional[str] = None):
        st.button(
            key=key,
            label="Cargar datos",
            type="primary",
            use_container_width=True,
            on_click=func
        )

    @execute_safely
    def download_df(self, df, file_name: str):
        st.download_button(
            label="Descargar 💾",
            data=df,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


class SelectBoxComponents:
    def __init__(self):
        ...

    @execute_safely
    def select_box_repuesto(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el repuesto:", RepuestoReparadoEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def select_box_tipo_repuesto(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el tipo de repuesto:", RepuestoEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def select_box_cabecera(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona la cabecera:", CabecerasEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def select_box_tipo_duracion(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el tipo de duración:", TipoDuracionEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def select_box_tipo_indice(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el tipo de índice:", IndexTypeEnum, index=0, key=key)

    @execute_safely
    def select_box_consumo_obligatorio(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el consumo obligatorio:", ConsumoObligatorioEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def select_box_load_data(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el dato a cargar:", LoadDataEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def select_box_rol(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el rol:", RoleEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def select_box_tipo_rep_comparacion(self, col, key: Union[int, str]):
        with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.selectbox("Selecciona el tipo de repuesto:", ConsumoComparacionRepuestoEnum, index=None,
                                placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def multi_select_box_tipo_rep_comparacion(self, col, key: Union[int, str]):
        with col.container(height=MULTI_SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.multiselect("Selecciona los tipos de repuestos:", ConsumoComparacionRepuestoEnum,
                                   placeholder=PLACEHOLDER, key=key)

    @execute_safely
    def multi_select_box_periodo(self, col, key: Union[int, str]):
        with col.container(height=MULTI_SELECT_BOX_HEIGHT, vertical_alignment='center'):
            return st.multiselect("Selecciona los períodos:", PeriodoComparacionEnum,
                                  placeholder=PLACEHOLDER, key=key)


class DialogComponents:

    def __init__(self):
        ...

    @st.dialog("Error")
    @execute_safely
    def error_dialog(self, message: str):
        st.write(message)


class OtherComponents:
    def __init__(self):
        ...

    @execute_safely
    def bar_tabs(self, contenedor_color: str, normal_text_color: str, normal_color: str, hover_color: str,
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

    @execute_safely
    def centered_title(self, col, title: str):
        with col.container(height=CENTERED_TITLE_HEIGHT, width=CENTERED_TITLE_WIDTH+250):
            st.markdown(f"<p style='text-align: center; font-size: 28px;'>{title}</p>", unsafe_allow_html=True)

    @execute_safely
    def mensaje_falta_rep(self, col):
        with col.container(height=SELECT_BOX_HEIGHT):
            st.text("No hay datos de este repuesto.")

    @execute_safely
    def custom_metric(self, col, label: str, value: Union[str, int, float], border_color: str, val_color: str,
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

    @execute_safely
    def flash_alert_success(self, mensaje: str) -> None:
        placeholder = st.empty()
        placeholder.success(mensaje)
        time.sleep(2)
        placeholder.empty()

    @execute_safely
    def flash_alert_error(self, mensaje: str) -> None:
        placeholder = st.empty()
        placeholder.error(mensaje)
        time.sleep(2)
        placeholder.empty()