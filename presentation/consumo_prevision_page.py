import time

import pandas as pd
import streamlit as st
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from config.constants_common import PAGE_STRFTIME_DMY, FILE_STRFTIME_YMD
from presentation.streamlit_components import SelectBoxComponents, OtherComponents, GoogleSheetsComponents
from utils.exception_utils import execute_safely

from viewmodels.consumo.prevision.plotter import PrevisionPlotter

from config.constants_views import (PLOT_BOX_HEIGHT, PAG_PREVISION, PREVISION_DF_KEY, PREVISION_SHEET_URL, PREVISION_COLS,
                                    PREVISION_EDITOR_KEY, PREVISION_FORECAST_COLS, PREVISION_REPUESTO_KEY,
                                    PREVISION_ULTIMO_REPUESTO_KEY, INDEX, PREVISION_STOCK_COLS,
                                    PREVISION_STOCK_EDITOR_KEY, SELECT_BOX_HEIGHT, DISTANCE_COLS_PREVISION, PLACEHOLDER,
                                    PREVISION_DF_CONSUMO_KEY, PREVISION_DF_STOCK_KEY)


class ConsumoPrevision:
    def __init__(self):
        self.select = SelectBoxComponents()
        self.other = OtherComponents()

    @execute_safely
    def page(self):
        st.title(PAG_PREVISION)
        config_col, articulo_col, _ = st.columns(DISTANCE_COLS_PREVISION)

        tipo_repuesto = self.select.select_box_tipo_repuesto(config_col, PREVISION_REPUESTO_KEY)
        google_sheet = GoogleSheetsComponents(PREVISION_SHEET_URL, tipo_repuesto, PREVISION_COLS)

        if tipo_repuesto:
            with st.spinner("Cargando datos..."):
                df_sheet = google_sheet.connect()

            pestaña_activa = st.segmented_control(
                "Vistas",
                options=["📈 Previsiones", "📑 Datos"],
                default="📈 Previsiones",
                label_visibility="collapsed"
            )

            if st.session_state.get(PREVISION_ULTIMO_REPUESTO_KEY) != tipo_repuesto:
                st.session_state[PREVISION_ULTIMO_REPUESTO_KEY] = tipo_repuesto
                st.session_state[PREVISION_DF_KEY] = df_sheet
                st.session_state[PREVISION_DF_STOCK_KEY] = df_sheet.copy()
                st.session_state[PREVISION_DF_CONSUMO_KEY] = df_sheet.copy()
            elif PREVISION_DF_KEY not in st.session_state:
                st.session_state[PREVISION_DF_KEY] = df_sheet
                st.session_state[PREVISION_DF_STOCK_KEY] = df_sheet.copy()
                st.session_state[PREVISION_DF_CONSUMO_KEY] = df_sheet.copy()

            if pestaña_activa == "📈 Previsiones":
                with st.spinner("Cargando gráficos de previsión..."):
                    _, titulo_centro_col, _ = st.columns((0.5, 1.2, 0.5))
                    _, centro_col, _ = st.columns((0.5, 3, 0.5))

                    if INDEX in df_sheet.columns:
                        df_sheet = df_sheet.drop(columns=[INDEX])

                    df_sheet.index = range(len(df_sheet))
                    # --------------------------------------------------------------------------

                    df_data = df_sheet[PREVISION_COLS].copy()
                    df_prevision = df_sheet[PREVISION_FORECAST_COLS].copy()
                    df_stock = df_sheet[PREVISION_STOCK_COLS].copy()

                    df_data["Mes"] = df_data["Mes"].apply(self.arreglar_fechas)
                    df_prevision["FechaPrevision"] = df_prevision["FechaPrevision"].apply(self.arreglar_fechas)

                    df_data = df_data.dropna(subset=["Mes"])
                    df_prevision = df_prevision.dropna(subset=["FechaPrevision"])

                    if not df_data.empty and not df_prevision.empty:
                        figs, titulo = PrevisionPlotter(df_data, df_prevision, df_stock, tipo_repuesto).create_plot()
                        self.other.centered_title(titulo_centro_col, titulo)

                        with centro_col:
                            for fig in figs:
                                with st.container(height=PLOT_BOX_HEIGHT):
                                    st.plotly_chart(fig)
                    else:
                        self.other.mensaje_falta_rep(centro_col)

            elif pestaña_activa == "📑 Datos":
                with articulo_col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
                    repuestos = st.session_state[PREVISION_DF_KEY]["RepuestoStock"].dropna().unique()
                    articulo_seleccionado = st.selectbox("Repuestos", repuestos, placeholder=PLACEHOLDER, index=None)

                if articulo_seleccionado:
                    df_stock_filtrado = st.session_state[PREVISION_DF_STOCK_KEY][
                        st.session_state[PREVISION_DF_STOCK_KEY]["RepuestoStock"] == articulo_seleccionado
                        ].copy()

                    df_consumo_filtrado = st.session_state[PREVISION_DF_CONSUMO_KEY][
                        st.session_state[PREVISION_DF_CONSUMO_KEY]["Articulo"] == articulo_seleccionado
                        ].copy()
                else:
                    df_stock_filtrado = st.session_state[PREVISION_DF_STOCK_KEY].copy()
                    df_consumo_filtrado = st.session_state[PREVISION_DF_CONSUMO_KEY].copy()

                stock_col, consumo_col = st.columns((1.8, 3))

                with stock_col:
                    key_dinamica_stock = f"{PREVISION_STOCK_EDITOR_KEY}_{tipo_repuesto}_{articulo_seleccionado}"

                    df_stock_filtrado["FechaStock"] = pd.to_datetime(df_stock_filtrado["FechaStock"],
                                                                     format='mixed',
                                                                     dayfirst=True,
                                                                     errors='coerce').dt.date
                    df_stock_filtrado["RepuestoStock"] = df_stock_filtrado["RepuestoStock"].fillna("").astype(str)

                    df_display_stock = df_stock_filtrado.reset_index(drop=True)

                    st.data_editor(
                        df_display_stock,
                        disabled=False,
                        num_rows="dynamic",
                        hide_index=True,
                        height=600,
                        key=key_dinamica_stock,
                        column_order=PREVISION_STOCK_COLS,
                        column_config={
                            "FechaStock": st.column_config.DateColumn("Fecha Stock", width=50,
                                                                      format="MM/YYYY"),
                            "RepuestoStock": st.column_config.TextColumn("Repuesto", width=150),
                            "StockActual": st.column_config.NumberColumn("Stock Actual", width=10),
                        }
                    )

                    _, centro_stock_guardar_col, _ = st.columns((1, 1.7, 1))

                    with centro_stock_guardar_col:
                        google_sheet.save_and_update_forecast(
                            df_filtrado=df_stock_filtrado,
                            celda_inicio="A2",
                            col_fin="C",
                            columnas_a_guardar=PREVISION_STOCK_COLS,
                            tipo_repuesto=tipo_repuesto,
                            dynamic_editor_key=key_dinamica_stock,
                            button_key="button_stock_key"
                        )

                with consumo_col:
                    key_dinamica_consumo = f"{PREVISION_EDITOR_KEY}_{tipo_repuesto}_{articulo_seleccionado}"

                    df_consumo_filtrado["Mes"] = pd.to_datetime(df_consumo_filtrado["Mes"],
                                                                format='mixed',
                                                                dayfirst=True,
                                                                errors='coerce').dt.date
                    df_consumo_filtrado["Articulo"] = df_consumo_filtrado["Articulo"].fillna("").astype(str)
                    df_consumo_filtrado["TipoRepuesto"] = df_consumo_filtrado["TipoRepuesto"].fillna("").astype(str)

                    df_display_consumo = df_consumo_filtrado.reset_index(drop=True)

                    st.data_editor(
                        df_display_consumo,
                        disabled=False,
                        num_rows="dynamic",
                        hide_index=True,
                        height=600,
                        key=key_dinamica_consumo,
                        column_order=PREVISION_COLS,
                        column_config={
                            "Mes": st.column_config.DateColumn("Fecha", width=50, format="MM/YYYY"),
                            "Articulo": st.column_config.SelectboxColumn("Repuesto", width=150,
                                                                         options=repuestos.tolist()),
                            "ConsumoMensual": st.column_config.TextColumn("Consumo Mensual", width=10),
                            "TipoRepuesto": st.column_config.TextColumn("Tipo Repuesto", width=60,
                                                                        default=tipo_repuesto),
                        }
                    )

                    _, centro_consumo_guardar_col, _ = st.columns((1, 0.85, 1))

                    with centro_consumo_guardar_col:
                        google_sheet.save_and_update_forecast(
                            df_filtrado=df_consumo_filtrado,
                            celda_inicio="E2",
                            col_fin="H",
                            columnas_a_guardar=PREVISION_COLS,
                            tipo_repuesto=tipo_repuesto,
                            dynamic_editor_key=key_dinamica_consumo,
                            button_key="button_consumo_key"
                        )
            else:
                with config_col:
                    st.write("Selecciona un repuesto.")


    @staticmethod
    def arreglar_fechas(fecha):
        try:
            if pd.isna(fecha) or str(fecha).strip() == "":
                return pd.NaT

            fecha_str = str(fecha).strip()

            if '/' in fecha_str:
                return pd.to_datetime(fecha_str, format=PAGE_STRFTIME_DMY, errors='coerce')
            elif '-' in fecha_str:
                fecha_str = fecha_str.split(" ")[0]
                return pd.to_datetime(fecha_str, format=FILE_STRFTIME_YMD, errors='coerce')
            else:
                return pd.to_datetime(fecha, errors='coerce')
        except Exception:
            return pd.NaT