import numpy as np
import streamlit as st

from config.constants_common import MODELOS_CHASIS, NORMAL_DATE_YMD, MARCAS_CHASIS, MARCAS_MOTOR, MODELOS_MOTOR, \
    CARROCERIAS, PARQUE_MOVIL_PAGER_KEY
from config.constants_views import PAG_PARQUE_MOVIL, PLACEHOLDER, FLOTA_CONTAINER_HEIGHT
from presentation.streamlit_components import Paginate
from viewmodels.datos_vm import ParqueMovilVM


class Filtros:
    pass


def parque_movil():
    paginate = Paginate()
    filtros = Filtros()

    st.title(PAG_PARQUE_MOVIL)

    _, fecha_desde_col, fecha_hasta_col, _ = st.columns([1,1,1,1])
    _, linea_col, dominio_col, interno_col, _ = st.columns([1,0.65,0.70,0.65,1])
    chasis_modelo_col, chasis_marca_col, motor_marca_col, motor_modelo_col, carroceria_col = st.columns([1,1,1,1,1])

    with fecha_desde_col.container(height=FLOTA_CONTAINER_HEIGHT):
        fecha_desde = st.date_input('Fecha desde', format=NORMAL_DATE_YMD, min_value="2010-01-01")

    with fecha_hasta_col.container(height=FLOTA_CONTAINER_HEIGHT):
        fecha_hasta = st.date_input('Fecha hasta', format=NORMAL_DATE_YMD, min_value="2010-01-01")

    with linea_col.container(height=FLOTA_CONTAINER_HEIGHT):
        linea = st.number_input("Linea", placeholder=PLACEHOLDER, format="%0f", icon="🚌", value=None)

    with interno_col.container(height=FLOTA_CONTAINER_HEIGHT):
        interno = st.number_input("Interno", placeholder=PLACEHOLDER, format="%0f", icon="👤", value=None)

    with dominio_col.container(height=FLOTA_CONTAINER_HEIGHT):
        dominio = st.text_input("Dominio", placeholder=PLACEHOLDER, icon="🚍")

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

    filtros.linea = linea
    filtros.interno = interno
    filtros.dominio = dominio
    filtros.modelo_chasis = modelo_chasis
    filtros.marca_chasis = marca_chasis
    filtros.modelo_motor = modelo_motor
    filtros.marca_motor = marca_motor
    filtros.carroceria = carroceria

    df = ParqueMovilVM().get_by_fechas(fecha_desde, fecha_hasta)
    mask = filtros_parque_movil(df, filtros)
    paginate.update_filters(filtros, "parque_movil", PARQUE_MOVIL_PAGER_KEY)

    df_paginado, paginas = paginate.create_pagination(df[mask], 15, PARQUE_MOVIL_PAGER_KEY)

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

    paginate.create_buttons(paginas, key=PARQUE_MOVIL_PAGER_KEY)


def filtros_parque_movil(df, filtros):
    mask = np.ones(len(df), dtype=bool)

    if filtros.linea:
        mask &= df["Linea"] == int(filtros.linea)

    if filtros.interno:
        mask &= df["Interno"] == int(filtros.interno)

    if filtros.dominio:
        mask &= df["Dominio"].str.startswith(filtros.dominio.strip().upper())

    if filtros.marca_chasis:
        mask &= df["ChasisMarca"].isin(filtros.marca_chasis)

    if filtros.modelo_chasis:
        mask &= df["ChasisModelo"].isin(filtros.modelo_chasis)

    if filtros.marca_motor:
        mask &= df["MotorMarca"].isin(filtros.marca_motor)

    if filtros.modelo_motor:
        mask &= df["MotorModelo"].isin(filtros.modelo_motor)

    if filtros.carroceria:
        mask &= df["Carroceria"].isin(filtros.carroceria)

    return mask