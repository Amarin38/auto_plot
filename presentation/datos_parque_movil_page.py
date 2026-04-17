import streamlit as st

from config.constants_common import MODELOS_CHASIS, NORMAL_DATE_YMD, MARCAS_CHASIS, MARCAS_MOTOR, MODELOS_MOTOR, \
    CARROCERIAS, TODAY_DATE_FILE_DMY
from config.constants_views import PAG_PARQUE_MOVIL, PLACEHOLDER, FLOTA_CONTAINER_HEIGHT
from domain.entities.parque_movil import ParqueMovilFiltro
from presentation.streamlit_components import OtherComponents, ButtonComponents
from utils.common_utils import CommonUtils
from viewmodels.common.parque_movil_vm import ParqueMovilVM


def parque_movil():
    other = OtherComponents()

    st.title(PAG_PARQUE_MOVIL)

    aux, fecha_desde_col, fecha_hasta_col, aux2 = st.columns([1,1,1,1])

    with fecha_desde_col.container(height=FLOTA_CONTAINER_HEIGHT):
        fecha_desde = st.date_input('Fecha desde', format=NORMAL_DATE_YMD, min_value="2000-01-01")

    with fecha_hasta_col.container(height=FLOTA_CONTAINER_HEIGHT):
        fecha_hasta = st.date_input('Fecha hasta', format=NORMAL_DATE_YMD, min_value="2000-01-01")


    aux, linea_col, dominio_col, interno_col, aux2 = st.columns([1,0.65,0.70,0.65,1])

    with linea_col.container(height=FLOTA_CONTAINER_HEIGHT):
        linea = st.number_input("Linea", placeholder=PLACEHOLDER, format="%0f", icon="🚌", value=None)

    with interno_col.container(height=FLOTA_CONTAINER_HEIGHT):
        interno = st.number_input("Interno", placeholder=PLACEHOLDER, format="%0f", icon="👤", value=None)

    with dominio_col.container(height=FLOTA_CONTAINER_HEIGHT):
        dominio = st.text_input("Dominio", placeholder=PLACEHOLDER, icon="🚍")


    chasis_modelo_col, chasis_marca_col, motor_marca_col, motor_modelo_col, carroceria_col = st.columns([1,1,1,1,1])

    with chasis_modelo_col.container(height=FLOTA_CONTAINER_HEIGHT):
        modelo_chasis = st.multiselect("Modelo de chasis", MODELOS_CHASIS)
        
    with chasis_marca_col.container(height=FLOTA_CONTAINER_HEIGHT):
        marca_chasis = st.multiselect("Marca de chasis", MARCAS_CHASIS)

    with motor_marca_col.container(height=FLOTA_CONTAINER_HEIGHT):
        marca_motor = st.multiselect("Marca de motor", MARCAS_MOTOR)

    with motor_modelo_col.container(height=FLOTA_CONTAINER_HEIGHT):
        modelo_motor = st.multiselect("Modelo de motor", MODELOS_MOTOR)

    with carroceria_col.container(height=FLOTA_CONTAINER_HEIGHT):
        carroceria = st.multiselect("Carroceria", CARROCERIAS)


    if ((fecha_desde and fecha_hasta) or linea or interno or
        dominio or modelo_chasis or marca_chasis or modelo_motor or
        marca_motor or carroceria_col):

        parque = ParqueMovilFiltro(linea, interno, dominio, marca_chasis, modelo_chasis,
                                   marca_motor, modelo_motor, carroceria)

        filtros_actuales = (fecha_desde, fecha_hasta,
                            linea, interno, dominio,
                            tuple(modelo_chasis), tuple(marca_chasis),
                            tuple(marca_motor), tuple(modelo_motor), tuple(carroceria))

        df = ParqueMovilVM().get_by_args(fecha_desde, fecha_hasta, parque)
        df_key = "df_completo"
        prev_filter_key = "filtros_previos"

        df_paginado, paginas = other.paginate(df, 15, df_key, "parque movil")

        if prev_filter_key not in st.session_state or st.session_state[prev_filter_key] != filtros_actuales:
            st.session_state[df_key+"_page"] = 0
            st.session_state[prev_filter_key] = filtros_actuales




        st.data_editor(
            df_paginado,
            disabled=True,
            hide_index=True,
            height=600,
            column_order=["FechaParqueMovil", "Linea", "Interno", "Dominio",
                          "Asientos", "Año", "ChasisMarca", "ChasisModelo", "ChasisNum",
                          "MotorMarca", "MotorModelo", "MotorNum", "Carroceria"],
            column_config={
                    "FechaParqueMovil"  : st.column_config.DateColumn("Fecha Parque Movil",
                                                                      format="localized", width=80),
                    "Linea"             : st.column_config.NumberColumn("Línea", width=30),
                    "Interno"           : st.column_config.NumberColumn("Interno", width=30),
                    "Dominio"           : st.column_config.TextColumn("Dominio", width=70),
                    "Asientos"          : st.column_config.NumberColumn("Asientos", width=30),
                    "Año"               : st.column_config.NumberColumn("Año", width=30),
                    "ChasisMarca"       : st.column_config.TextColumn("Marca Chasis", width=60),
                    "ChasisModelo"      : st.column_config.TextColumn("Modelo Chasis", width=60),
                    "ChasisNum"         : st.column_config.TextColumn("Número Chasis", width=85),
                    "MotorMarca"        : st.column_config.TextColumn("Marca Motor", width=60),
                    "MotorModelo"       : st.column_config.TextColumn("Modelo Motor", width=60),
                    "MotorNum"          : st.column_config.TextColumn("Número Motor", width=60),
                    "Carroceria"        : st.column_config.TextColumn("Carrocería", width=60),
                }
            )

        other.paginate_buttons(paginas, key=df_key)

