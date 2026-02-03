from datetime import date

import streamlit as st

from config.constants_common import MODELOS_CHASIS, NORMAL_DATE_YMD, MARCAS_CHASIS, MARCAS_MOTOR, MODELOS_MOTOR, \
    CARROCERIAS
from config.constants_views import PAG_PARQUE_MOVIL, PLACEHOLDER, FLOTA_CONTAINER_HEIGHT
from domain.entities.parque_movil import ParqueMovilFiltro
from utils.common_utils import CommonUtils
from viewmodels.common.parque_movil_vm import ParqueMovilVM

@st.cache_data(ttl=300, show_spinner="Cargando parque movil...", show_time=True)
def _obtener_parque_movil(fecha_desde: date, fecha_hasta: date, parque: ParqueMovilFiltro):
    return ParqueMovilVM().get_by_args(fecha_desde, fecha_hasta, parque)


def parque_movil():
    utils = CommonUtils()
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

        if "filtros_previos" not in st.session_state or st.session_state.filtros_previos != filtros_actuales:
            st.session_state.df_completo = None
            st.session_state.page = 0
            st.session_state.filtros_previos = filtros_actuales

        if st.session_state.df_completo is None:
            resultado = utils.run_in_threads(lambda: _obtener_parque_movil(fecha_desde, fecha_hasta, parque),
                                             max_workers=6)
            st.session_state.df_completo = resultado

        if st.session_state.df_completo is not None:
            if "page" not in st.session_state:
                st.session_state.page = 0

            df = st.session_state.df_completo

            # Config de la paginacion:
            items_por_pagina = 15
            total_items = len(df)
            total_paginas = max(1, (total_items + items_por_pagina - 1) // items_por_pagina)

            # Calcular indices
            inicio = st.session_state.page * items_por_pagina
            fin = min(inicio + items_por_pagina, total_items)

            st.data_editor(
                df.iloc[inicio:fin],
                disabled=True,
                hide_index=True,
                height=600,
                # num_rows="dynamic",
                key=f"editor_page_{st.session_state.page}",
                column_order=["FechaParqueMovil", "Linea", "Interno", "Dominio",
                                         "Asientos", "Año", "ChasisMarca", "ChasisModelo", "ChasisNum",
                                         "MotorMarca", "MotorModelo", "MotorNum", "Carroceria"],
                column_config={
                        "FechaParqueMovil": st.column_config.DateColumn("Fecha Parque Movil",
                                                                        format="localized", width=80),
                        "Linea": st.column_config.NumberColumn("Línea", width=30),
                        "Interno": st.column_config.NumberColumn("Interno", width=30),
                        "Dominio": st.column_config.TextColumn("Dominio", width=70),
                        "Asientos": st.column_config.NumberColumn("Asientos", width=30),
                        "Año": st.column_config.NumberColumn("Año", width=30),
                        "ChasisMarca": st.column_config.TextColumn("Marca Chasis", width=60),
                        "ChasisModelo": st.column_config.TextColumn("Modelo Chasis", width=60),
                        "ChasisNum": st.column_config.TextColumn("Número Chasis", width=85),
                        "MotorMarca": st.column_config.TextColumn("Marca Motor", width=60),
                        "MotorModelo": st.column_config.TextColumn("Modelo Motor", width=60),
                        "MotorNum": st.column_config.TextColumn("Número Motor", width=60),
                        "Carroceria": st.column_config.TextColumn("Carrocería", width=60),
                    }
                )

            # Actualizo el dataframe completo con los cambios
            col1, col2, col3 = st.columns([5.5,4.5,1])
            with col1:
                if st.button('← Anterior', disabled=st.session_state.page == 0):
                    st.session_state.page -= 1
                    st.rerun()

            with col2:
                st.write(f'Página {st.session_state.page + 1} de {total_paginas}')

            with col3:
                if st.button('Siguiente →', disabled=st.session_state.page >= total_paginas - 1, width=150):
                    st.session_state.page += 1
                    st.rerun()

            if st.button('Ver datos completos'):
                st.dataframe(st.session_state.df_completo)
        else:
            st.dataframe()