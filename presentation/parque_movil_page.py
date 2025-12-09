import streamlit as st

from config.constants_common import MODELOS_CHASIS, NORMAL_DATE_YMD, MARCAS_CHASIS, MARCAS_MOTOR, MODELOS_MOTOR, \
    CARROCERIAS
from config.constants_views import PAG_PARQUE_MOVIL, PLACEHOLDER, FLOTA_CONTAINER_HEIGHT
from domain.entities.parque_movil import ParqueMovil, ParqueMovilFiltro
from viewmodels.common.parque_movil_vm import ParqueMovilVM


def parque_movil():
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


    if ((fecha_desde and fecha_hasta) or
        linea or interno or dominio or modelo_chasis or
        marca_chasis or modelo_motor or marca_motor or carroceria_col):

        parque = ParqueMovilFiltro(linea, interno, dominio, marca_chasis,
                                   modelo_chasis, marca_motor, modelo_motor, carroceria)

        datos_parque = ParqueMovilVM().get_by_args(fecha_desde, fecha_hasta, parque)

        if datos_parque is not None:
            st.dataframe(datos_parque, hide_index=True,
                         column_config={
                             "FechaParqueMovil": st.column_config.DateColumn("FechaParqueMovil",
                                                                             format="localized"),
                         },
                         height=650)
        else:
            st.dataframe()