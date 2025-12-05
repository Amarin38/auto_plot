import streamlit as st

from config.constants_common import MODELOS_CHASIS, NORMAL_DATE_YMD, MARCAS_CHASIS, MARCAS_MOTOR, MODELOS_MOTOR, \
    CARROCERIAS
from config.constants_views import PAG_PARQUE_MOVIL, PLACEHOLDER
from viewmodels.common.parque_movil_vm import ParqueMovilVM


def parque_movil():
    st.title(PAG_PARQUE_MOVIL)


    aux, fecha_desde_col, fecha_hasta_col, aux2 = st.columns([1,1,1,1])

    with fecha_desde_col.container(height=100):
        fecha_desde = st.date_input('Fecha desde', format=NORMAL_DATE_YMD, min_value="2000-01-01")


    with fecha_hasta_col.container(height=100):
        fecha_hasta = st.date_input('Fecha hasta', format=NORMAL_DATE_YMD, min_value="2000-01-01")



    aux, linea_col, interno_col, dominio_col, modelo_chasis_col, aux2 = st.columns([1,0.75, 0.75, 0.75, 0.75,1])

    with linea_col.container(height=100):
        linea = st.text_input("Linea", placeholder=PLACEHOLDER)

    with interno_col.container(height=100):
        interno = st.text_input("Interno", placeholder=PLACEHOLDER)

    with dominio_col.container(height=100):
        dominio = st.text_input("Dominio", placeholder=PLACEHOLDER)

    with modelo_chasis_col.container(height=100):
        modelo_chasis = st.multiselect("Modelo de chasis", MODELOS_CHASIS)


    aux, chasis_marca_col, marca_motor_col, modelo_motor_col, carroceria_col, aux2 = st.columns([1,0.75, 0.75, 0.75, 0.75,1])

    # TODO agregar los filtros de abajo:
    with chasis_marca_col.container(height=100):
        marca_chasis = st.multiselect("Marca de chasis", MARCAS_CHASIS)

    with marca_motor_col.container(height=100):
        marca_motor = st.multiselect("Marca de motor", MARCAS_MOTOR)

    with modelo_motor_col.container(height=100):
        modelo_motor = st.multiselect("Modelo de motor", MODELOS_MOTOR)

    with carroceria_col.container(height=100):
        carroceria_col = st.multiselect("Carroceria", CARROCERIAS)


    if (fecha_desde and fecha_hasta) or linea or interno or dominio or modelo_chasis:
        st.dataframe(ParqueMovilVM().get_by_args(fecha_desde, fecha_hasta, linea, interno, dominio, modelo_chasis),
                     hide_index=True,
                     column_config={
                         "FechaParqueMovil": st.column_config.DateColumn("FechaParqueMovil",
                                                                         format="localized"),
                     },
                     height=650)

