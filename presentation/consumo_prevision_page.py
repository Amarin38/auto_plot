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

        prevision_tab, datos_tab = st.tabs(["📈 Previsiones", "📑 Datos"])

        tipo_repuesto = self.select.select_box_tipo_repuesto(config_col, PREVISION_REPUESTO_KEY)
        google_sheet = GoogleSheetsComponents(PREVISION_SHEET_URL, tipo_repuesto, PREVISION_COLS)
        df_sheet = google_sheet.connect()

        with prevision_tab:
            _, titulo_centro_col, _ = st.columns((0.5, 1, 0.5))
            _, centro_col, _ = st.columns((0.5, 3, 0.5))

            if tipo_repuesto:
                if INDEX in df_sheet.columns:
                    df_sheet = df_sheet.drop(columns=[INDEX])

                df_sheet.index = range(len(df_sheet))

                if st.session_state.get(PREVISION_ULTIMO_REPUESTO_KEY) != tipo_repuesto:
                    st.session_state[PREVISION_ULTIMO_REPUESTO_KEY] = tipo_repuesto
                    st.session_state[PREVISION_DF_KEY] = df_sheet
                    st.session_state[PREVISION_DF_STOCK_KEY] = df_sheet.copy()
                    st.session_state[PREVISION_DF_CONSUMO_KEY] = df_sheet.copy()
                elif PREVISION_DF_KEY not in st.session_state:
                    st.session_state[PREVISION_DF_KEY] = df_sheet
                    st.session_state[PREVISION_DF_STOCK_KEY] = df_sheet.copy()
                    st.session_state[PREVISION_DF_CONSUMO_KEY] = df_sheet.copy()
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
            else:
                with config_col:
                    st.write("Selecciona un repuesto.")

        with datos_tab:
            if st.toggle("Actualizar datos") and tipo_repuesto:
                with articulo_col.container(height=SELECT_BOX_HEIGHT):
                    repuestos = st.session_state[PREVISION_DF_KEY]["RepuestoStock"].dropna().unique()
                    articulo_seleccionado = st.selectbox("Repuestos", repuestos, placeholder=PLACEHOLDER, index=None)

                if articulo_seleccionado:
                    df_stock_filtrado = st.session_state[PREVISION_DF_STOCK_KEY][
                        st.session_state[PREVISION_DF_STOCK_KEY]["RepuestoStock"] == articulo_seleccionado
                        ]

                    df_consumo_filtrado = st.session_state[PREVISION_DF_CONSUMO_KEY][
                        st.session_state[PREVISION_DF_CONSUMO_KEY]["Articulo"] == articulo_seleccionado
                        ]
                else:
                    df_stock_filtrado = st.session_state[PREVISION_DF_STOCK_KEY]
                    df_consumo_filtrado = st.session_state[PREVISION_DF_CONSUMO_KEY]

                stock_col, consumo_col = st.columns((1.8, 3))

                with stock_col:
                    key_dinamica_stock = f"{PREVISION_STOCK_EDITOR_KEY}_{tipo_repuesto}_{articulo_seleccionado}"

                    df_stock_filtrado["FechaStock"] = pd.to_datetime(df_stock_filtrado["FechaStock"],
                                                                     format='mixed',
                                                                     dayfirst=True,
                                                                     errors='coerce').dt.date
                    df_stock_filtrado["RepuestoStock"] = df_stock_filtrado["RepuestoStock"].fillna("").astype(str)

                    df_modificado_stock = st.data_editor(
                        df_stock_filtrado,
                        disabled=False,
                        num_rows="dynamic",
                        height=600,
                        key=key_dinamica_stock,
                        column_order=PREVISION_STOCK_COLS,
                        column_config={
                            "FechaStock": st.column_config.DateColumn("Fecha Stock", width=50, format="DD/MM/YYYY"),
                            "RepuestoStock": st.column_config.TextColumn("Repuesto", width=150),
                            "StockActual": st.column_config.NumberColumn("Stock Actual", width=10),
                        }
                    )

                    _, centro_stock_guardar_col, _ = st.columns((1, 3, 0.5))

                    with centro_stock_guardar_col:
                        if st.button("💾 Guardar cambios de stock"):
                            df_completo = google_sheet.update_filtered_df(key_dinamica_stock,
                                                                          PREVISION_DF_KEY,
                                                                          df_stock_filtrado)

                            if "FechaStock" in df_completo.columns:
                                df_completo["FechaStock"] = pd.to_datetime(df_completo["FechaStock"],
                                                                           format='mixed',
                                                                           dayfirst=True,
                                                                           errors='coerce').dt.strftime('%d/%m/%Y')

                            google_sheet.save_and_update_forecast(
                                df_modificado=df_completo,
                                df_consumo=df_completo if "Articulo" in df_completo.columns else st.session_state[PREVISION_DF_CONSUMO_KEY],
                                df_stock=df_completo if "RepuestoStock" in df_completo.columns else st.session_state[PREVISION_DF_STOCK_KEY],
                                tipo_repuesto=tipo_repuesto,
                                df_key=PREVISION_DF_KEY,
                                editor_key=key_dinamica_stock,
                                celda_inicio="A2",
                                col_fin="C",
                                columnas_a_guardar=PREVISION_STOCK_COLS
                            )

                with consumo_col:
                    key_dinamica_consumo = f"{PREVISION_EDITOR_KEY}_{tipo_repuesto}_{articulo_seleccionado}"

                    df_consumo_filtrado["Mes"] = pd.to_datetime(df_consumo_filtrado["Mes"],
                                                                format='mixed',
                                                                dayfirst=True,
                                                                errors='coerce').dt.date
                    df_consumo_filtrado["Articulo"] = df_consumo_filtrado["Articulo"].fillna("").astype(str)
                    df_consumo_filtrado["TipoRepuesto"] = df_consumo_filtrado["TipoRepuesto"].fillna("").astype(str)

                    df_modificado_consumo = st.data_editor(
                        df_consumo_filtrado,
                        disabled=False,
                        num_rows="dynamic",
                        height=600,
                        key=key_dinamica_consumo,
                        column_order=PREVISION_COLS,
                        column_config={
                            "Mes": st.column_config.DateColumn("Fecha", width=50, format="MM/YYYY"),
                            "Articulo": st.column_config.SelectboxColumn("Repuesto", width=150, options=repuestos.tolist()),
                            "ConsumoMensual": st.column_config.TextColumn("Consumo Mensual", width=10),
                            "TipoRepuesto": st.column_config.TextColumn("Tipo Repuesto", width=60, default=tipo_repuesto),
                        }
                    )

                    _, centro_consumo_guardar_col, _ = st.columns((2.5, 3, 0.5))

                    with centro_consumo_guardar_col:
                        if st.button("💾 Guardar cambios de consumo"):
                            df_completo = google_sheet.update_filtered_df(key_dinamica_consumo,
                                                                          PREVISION_DF_KEY,
                                                                          df_consumo_filtrado)

                            if "Mes" in df_completo.columns:
                                df_completo["Mes"] = pd.to_datetime(df_completo["Mes"],
                                                                    format='mixed',
                                                                    dayfirst=True,
                                                                    errors='coerce')

                                df_completo["Mes"] = df_completo["Mes"].dt.to_period('M').dt.to_timestamp().dt.strftime('%d/%m/%Y')

                            google_sheet.save_and_update_forecast(
                                df_modificado=df_completo,
                                df_consumo=df_completo if "Articulo" in df_completo.columns else st.session_state[PREVISION_DF_CONSUMO_KEY],
                                df_stock=df_completo if "RepuestoStock" in df_completo.columns else st.session_state[PREVISION_DF_STOCK_KEY],
                                tipo_repuesto=tipo_repuesto,
                                df_key=PREVISION_DF_KEY,
                                editor_key=key_dinamica_consumo,
                                celda_inicio="E2",
                                col_fin="H",
                                columnas_a_guardar=PREVISION_COLS
                            )


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