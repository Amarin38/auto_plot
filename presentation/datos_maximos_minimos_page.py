from operator import index

import numpy as np
import streamlit as st
import pandas as pd

from config.constants_common import MAX_MIN_SHEET_URL, MAX_MIN_SHEET_COLS, MAX_MIN_CABECERA_KEY, MAX_MIN_DF_KEY, \
    MAX_MIN_DF_STOCK_KEY, INDEX, MAX_MIN_STOCK_COLS, MAX_MIN_TABLE_KEY, MAX_MIN_EDITOR_KEY, MAX_MIN_PAGER_KEY
from config.constants_views import PAG_MAXIMOS_MINIMOS, PLACEHOLDER, SELECT_BOX_HEIGHT
from config.enums import CabecerasEnum
from domain.services.compute_datos_maximos_minimos import calculate_maxmin

from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents, GoogleSheetsComponents, OtherComponents


class Filtros:
    pass

google_sheet = GoogleSheetsComponents(MAX_MIN_SHEET_URL, "Hoja 1", MAX_MIN_STOCK_COLS)

@st.cache_data(ttl=200, show_spinner=True)
def get_sheet():
    return google_sheet.connect()

@execute_safely
def maximos_minimos():
    DATE_FMT = "%Y-%m-%d"
    select = SelectBoxComponents()
    other = OtherComponents()


    st.title(PAG_MAXIMOS_MINIMOS)

    cabecera_col, familia_col, articulo_col, descripcion_col = st.columns([1, 1, 1, 1])
    cabecera_seleccionada = select.select_box_cabecera(cabecera_col, "MAX_MIN_CABECERA")

    if cabecera_seleccionada:
        pestaña_activa = st.segmented_control(
            "Vistas",
            options=["↕️ Máximos y Mínimos", "📑 Datos"],
            default="↕️ Máximos y Mínimos",
            label_visibility="collapsed"
        )

        with familia_col.container(height=SELECT_BOX_HEIGHT):
            familia = st.text_input("Familia", placeholder=PLACEHOLDER, icon="🛠️")

        with articulo_col.container(height=SELECT_BOX_HEIGHT):
            articulo = st.text_input("Artículo", placeholder=PLACEHOLDER, icon="🪛")

        with descripcion_col.container(height=SELECT_BOX_HEIGHT):
            descripcion = st.text_input("Descripción", placeholder=PLACEHOLDER, icon="📑")

        df_sheet = get_sheet()
        filtros = Filtros()

        filtros.familia = familia
        filtros.articulo = articulo
        filtros.descripcion = descripcion

        if st.session_state.get(MAX_MIN_CABECERA_KEY) != cabecera_seleccionada:
            st.session_state[MAX_MIN_CABECERA_KEY] = cabecera_seleccionada
            st.session_state[MAX_MIN_DF_KEY] = df_sheet
            st.session_state[MAX_MIN_DF_STOCK_KEY] = df_sheet.copy()
        elif MAX_MIN_DF_KEY not in st.session_state:
            st.session_state[MAX_MIN_DF_KEY] = df_sheet
            st.session_state[MAX_MIN_DF_STOCK_KEY] = df_sheet.copy()

        if INDEX in df_sheet.columns:
            df_sheet = df_sheet.drop(columns=[INDEX])

        df_sheet.index = range(len(df_sheet))

        # -------------------------------------------------------------------------------
        df_max_min   = df_sheet[MAX_MIN_SHEET_COLS].copy()
        df_stock     = df_sheet[MAX_MIN_STOCK_COLS].copy()

        dynamic_key_max_min         = f"{MAX_MIN_TABLE_KEY}_{cabecera_seleccionada}"
        dynamic_key_stock_max_min   = f"{MAX_MIN_EDITOR_KEY}_{cabecera_seleccionada}"

        # -------------------------------------------------------------------------------

        df_max_min_filtrado = st.session_state[MAX_MIN_DF_KEY][
            st.session_state[MAX_MIN_DF_KEY]["Cabecera"] == cabecera_seleccionada
        ].copy()

        df_max_min_filtrado["Descripcion"] = df_max_min_filtrado["Descripcion"].fillna("").astype(str)
        df_max_min_filtrado["Cabecera"] = df_max_min_filtrado["Cabecera"].astype("category")
        df_max_min_filtrado["Familia"] = df_max_min_filtrado["Familia"].astype("uint16")
        df_max_min_filtrado["Articulo"] = df_max_min_filtrado["Articulo"].astype("uint32")
        df_max_min_filtrado["Fecha"] = pd.to_datetime(
            df_max_min_filtrado["Fecha"],
            format='mixed',
            dayfirst=True,
            errors='coerce'
        ).dt.date

        # Filtros
        mask_max_min = np.ones(len(df_max_min_filtrado), dtype=bool)

        if filtros.familia:
            mask_max_min &= df_max_min_filtrado["Familia"] == int(filtros.familia.strip())

        if filtros.articulo:
            mask_max_min &= df_max_min_filtrado["Articulo"] == int(filtros.articulo.strip())

        if filtros.descripcion:
            mask_max_min &= df_max_min_filtrado["Descripcion"].str.startswith(str(filtros.descripcion.strip().upper()))

        df_max_min_filtrado = df_max_min_filtrado[mask_max_min]

        df_max_min_filtrado = df_max_min_filtrado.sort_values(
            by=["Familia", "Articulo", "Fecha"],
            ascending=[True, True, True]
        ).copy()

        other.actualizar_filtros_paginate(filtros, "maxmin", MAX_MIN_PAGER_KEY)

        # -------------------------------------------------------------------------------

        df_stock_filtrado = st.session_state[MAX_MIN_DF_STOCK_KEY][
            st.session_state[MAX_MIN_DF_STOCK_KEY]["CabeceraStock"] == cabecera_seleccionada
        ].copy()

        df_stock_filtrado["DescripcionStock"] = df_stock_filtrado["DescripcionStock"].fillna("").astype(str)
        df_stock_filtrado["CabeceraStock"] = df_stock_filtrado["CabeceraStock"].astype("category")
        df_stock_filtrado["FamiliaStock"] = df_stock_filtrado["FamiliaStock"].astype("uint16")
        df_stock_filtrado["ArticuloStock"] = df_stock_filtrado["ArticuloStock"].astype("uint32")
        df_stock_filtrado["FechaStock"] = pd.to_datetime(
            df_stock_filtrado["FechaStock"],
            format='mixed',
            dayfirst=True,
            errors='coerce'
        ).dt.date

        # Filtros
        mask_max_min_stock = np.ones(len(df_stock_filtrado), dtype=bool)

        if filtros.familia:
            mask_max_min_stock &= df_stock_filtrado["FamiliaStock"] == int(filtros.familia.strip())

        if filtros.articulo:
            mask_max_min_stock &= df_stock_filtrado["ArticuloStock"] == int(filtros.articulo.strip())

        if filtros.descripcion:
            mask_max_min_stock &= df_stock_filtrado["DescripcionStock"].str.startswith(str(filtros.descripcion.strip().upper()))

        df_stock_filtrado = df_stock_filtrado[mask_max_min_stock]

        df_stock_filtrado = df_stock_filtrado.sort_values(
            by=["FamiliaStock", "ArticuloStock", "FechaStock"],
            ascending=[True, True, True]
        ).copy()

        # -------------------------------------------------------------------------------

        df_display_stock_max_min = df_stock_filtrado.reset_index(drop=True)

        if pestaña_activa == "↕️ Máximos y Mínimos":
            if len(df_max_min):
                df_paginado, paginas = other.paginate(df_max_min_filtrado, 15, MAX_MIN_PAGER_KEY, False)
                df_display_max_min = df_paginado.reset_index(drop=True)

                st.data_editor(
                    df_display_max_min,
                    disabled=True,
                    hide_index=True,
                    height=600,
                    key=dynamic_key_max_min,
                    column_order=MAX_MIN_SHEET_COLS,
                    column_config={
                        "Familia": st.column_config.NumberColumn("Familia"),
                        "Articulo": st.column_config.NumberColumn("Artículo"),
                        "Decripcion": st.column_config.TextColumn("Decripcion"),
                        "Cabecera": st.column_config.TextColumn("Cabecera"),
                        "Fecha": st.column_config.DateColumn("Fecha"),
                        "Minimo": st.column_config.NumberColumn("Mínimo"),
                        "Maximo": st.column_config.NumberColumn("Máximo"),
                    }
                )

                other.paginate_buttons(paginas, key=MAX_MIN_PAGER_KEY)

        elif pestaña_activa == "📑 Datos":
            if len(df_stock):
                st.data_editor(
                    df_display_stock_max_min,
                    disabled=False,
                    num_rows="dynamic",
                    hide_index=True,
                    height=600,
                    key=dynamic_key_stock_max_min,
                    column_order=MAX_MIN_STOCK_COLS,
                    column_config={
                        "FamiliaStock": st.column_config.NumberColumn("Familia"),
                        "ArticuloStock": st.column_config.NumberColumn("Artículo"),
                        "DescripcionStock": st.column_config.TextColumn("Decripción"),
                        "CabeceraStock": st.column_config.SelectboxColumn("Cabecera", options=CabecerasEnum),
                        "FechaStock": st.column_config.DateColumn("Fecha"),
                        "Stock": st.column_config.NumberColumn("Stock"),
                    }
                )

                boton_guardar, min_input, max_input, _ = st.columns((1.1, 1, 1, 6))

                minimo = min_input.number_input("Mínimo", min_value=0.1, value=1.0)
                maximo = max_input.number_input("Máximo", min_value=0.1, value=2.0)

                def guardar_calculos_automaticos(df_stock_actualizado):
                    with st.spinner("Recalculando Máximos y Mínimos..."):
                        with st.spinner(f"Recalculando y actualizando {cabecera_seleccionada}..."):
                            df_stock_solo_cabecera = df_stock_actualizado[
                                df_stock_actualizado["CabeceraStock"] == cabecera_seleccionada
                            ].copy()

                            df_calculado_nuevo = calculate_maxmin(df_stock_solo_cabecera, minimo, maximo)
                            df_maestro_maxmin = st.session_state[MAX_MIN_DF_KEY].copy()

                            df_maestro_limpio = df_maestro_maxmin[
                                (df_maestro_maxmin["Cabecera"] != cabecera_seleccionada) &
                                (df_maestro_maxmin["Cabecera"].astype(str).str.strip() != "") &
                                (df_maestro_maxmin["Cabecera"].astype(str).str.lower() != "nan")
                            ].copy()

                            df_final_actualizado = pd.concat([df_maestro_limpio, df_calculado_nuevo], ignore_index=True)

                            st.session_state[MAX_MIN_DF_KEY] = df_final_actualizado

                            df_para_guardar = df_final_actualizado[MAX_MIN_SHEET_COLS].copy()
                            df_para_guardar.loc[:, "Fecha"] = pd.to_datetime(df_para_guardar["Fecha"], errors="coerce", format=DATE_FMT)

                            google_sheet.save_full(
                                df=df_para_guardar,
                                rango="H2:N",
                            )

                            get_sheet.clear()

                google_sheet.save_partial(
                    df_paginado=df_stock_filtrado,
                    df_key=MAX_MIN_DF_STOCK_KEY,
                    editor_key=dynamic_key_stock_max_min,
                    rango="A2:F",
                    button_col=boton_guardar,
                    button_key="STOCK_BUTTON",
                    after_save=guardar_calculos_automaticos,
                )
