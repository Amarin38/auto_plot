import streamlit as st
import pandas as pd

from config.constants_common import MAX_MIN_SHEET_URL, MAX_MIN_SHEET_COLS, MAX_MIN_CABECERA_KEY, MAX_MIN_DF_KEY, \
    MAX_MIN_DF_STOCK_KEY, INDEX, MAX_MIN_STOCK_COLS, MAX_MIN_TABLE_KEY, MAX_MIN_EDITOR_KEY
from config.constants_views import PAG_MAXIMOS_MINIMOS
from config.enums import CabecerasEnum
from domain.services.compute_datos_maximos_minimos import calculate_maxmin

from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents, GoogleSheetsComponents

@execute_safely
def maximos_minimos():
    DATE_FMT = "%Y-%m-%d"
    select = SelectBoxComponents()

    st.title(PAG_MAXIMOS_MINIMOS)

    cabecera, _ = st.columns([0.6, 2])
    cabecera_seleccionada = select.select_box_cabecera(cabecera, "MAX_MIN_CABECERA")
    google_sheet = GoogleSheetsComponents(MAX_MIN_SHEET_URL, "Hoja 1", MAX_MIN_STOCK_COLS)

    if cabecera_seleccionada:
        with st.spinner("Cargando datos..."):
            df_sheet = google_sheet.connect()

        pestaña_activa = st.segmented_control(
            "Vistas",
            options=["↕️ Máximos y Mínimos", "📑 Datos"],
            default="↕️ Máximos y Mínimos",
            label_visibility="collapsed"
        )

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

        # --------------------------------------------------------------------------
        df_max_min  = df_sheet[MAX_MIN_SHEET_COLS].copy()
        df_stock     = df_sheet[MAX_MIN_STOCK_COLS].copy()

        dynamic_key_max_min         = f"{MAX_MIN_TABLE_KEY}_{cabecera_seleccionada}"
        dynamic_key_stock_max_min   = f"{MAX_MIN_EDITOR_KEY}_{cabecera_seleccionada}"

        df_max_min_filtrado = st.session_state[MAX_MIN_DF_KEY][
            st.session_state[MAX_MIN_DF_KEY]["Cabecera"] == cabecera_seleccionada
        ].copy()

        df_stock_filtrado = st.session_state[MAX_MIN_DF_STOCK_KEY][
            st.session_state[MAX_MIN_DF_STOCK_KEY]["CabeceraStock"] == cabecera_seleccionada
        ].copy()

        df_max_min_filtrado["Fecha"] = pd.to_datetime(
            df_max_min_filtrado["Fecha"],
            format='mixed',
            dayfirst=True,
            errors='coerce'
        ).dt.date

        df_stock_filtrado["FechaStock"] = pd.to_datetime(
            df_stock_filtrado["FechaStock"],
            format='mixed',
            dayfirst=True,
            errors='coerce'
        ).dt.date

        df_display_max_min       = df_max_min_filtrado.reset_index(drop=True)
        df_display_stock_max_min = df_stock_filtrado.reset_index(drop=True)

        df_display_max_min["Cabecera"] = df_display_max_min["Cabecera"].fillna("").astype(str)
        df_display_max_min["Descripcion"] = df_display_max_min["Descripcion"].fillna("").astype(str)

        df_display_stock_max_min["CabeceraStock"] = df_display_stock_max_min["CabeceraStock"].fillna("").astype(str)
        df_display_stock_max_min["DescripcionStock"] = df_display_stock_max_min["DescripcionStock"].fillna("").astype(str)

        if pestaña_activa == "↕️ Máximos y Mínimos":
            if len(df_max_min):
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

                minimo = min_input.number_input("Mínimo", min_value=1, value=1)
                maximo = max_input.number_input("Máximo", min_value=1, value=2)

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
                            df_para_guardar = df_final_actualizado[MAX_MIN_SHEET_COLS]
                            df_para_guardar["Fecha"] = pd.to_datetime(df_para_guardar["Fecha"], errors="coerce", format=DATE_FMT)

                            google_sheet.save_full(
                                df=df_para_guardar,
                                rango="H2:N100000",
                            )

                google_sheet.save_partial(
                    df_paginado=df_stock_filtrado,
                    df_key=MAX_MIN_DF_STOCK_KEY,
                    editor_key=dynamic_key_stock_max_min,
                    rango="A2:F100000",
                    button_col=boton_guardar,
                    button_key="STOCK_BUTTON",
                    after_save=guardar_calculos_automaticos,
                )
