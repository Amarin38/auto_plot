import pandas as pd
import streamlit as st

from config.constants_common import PAGE_STRFTIME_DMY, FILE_STRFTIME_YMD
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from presentation.streamlit_components import SelectBoxComponents, OtherComponents, GoogleSheetsComponents
from utils.exception_utils import execute_safely
from viewmodels.consumo.prevision.data_vm import PrevisionDataVM

from viewmodels.consumo.prevision.plotter import PrevisionPlotter

from config.constants_views import (PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE, DISTANCE_COLS_SELECTBIGGER_PLOT,
                                    PAG_PREVISION, PREVISION_DF_KEY, PREVISION_SHEET_URL, PREVISION_COLS,
                                    PREVISION_EDITOR_KEY, PREVISION_FORECAST_COLS,
                                    PREVISION_REPUESTO_KEY, PREVISION_ULTIMO_REPUESTO_KEY, INDEX, PREVISION_STOCK_COLS,
                                    PREVISION_STOCK_EDITOR_KEY)
from viewmodels.consumo.prevision.vm import PrevisionVM


class ConsumoPrevision:
    def __init__(self):
        self.select = SelectBoxComponents()
        self.other = OtherComponents()

    @staticmethod
    @st.cache_data(ttl=200, show_spinner=False, show_time=True)
    def _cargar_datos(tipo_repuesto):
        uow = SQLAlchemyUnitOfWork()
        return PrevisionDataVM(uow=uow).get_df_by_tipo_repuesto(tipo_repuesto), PrevisionVM(
            uow=uow).get_df_by_tipo_repuesto(tipo_repuesto)


    @execute_safely
    def page(self):
        st.title(PAG_PREVISION)
        config_col, _ = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

        prevision_tab, datos_tab = st.tabs(["📈 Previsiones", "📑 Datos"])

        tipo_repuesto = self.select.select_box_tipo_repuesto(config_col, PREVISION_REPUESTO_KEY)
        google_sheet = GoogleSheetsComponents(PREVISION_SHEET_URL, tipo_repuesto, PREVISION_COLS)
        df_sheet = google_sheet.connect()

        with prevision_tab:
            _, titulo_centro_col, _ = st.columns((0.5, 1, 0.5))
            _, centro_col, _ = st.columns((0.5, 3, 0.5))

            if tipo_repuesto:
                df_stock = df_sheet[["RepuestoStock", "StockActual"]]

                if INDEX in df_sheet.columns:
                    df_sheet = df_sheet.drop(columns=[INDEX])

                df_sheet.index = range(len(df_sheet))

                if st.session_state.get(PREVISION_ULTIMO_REPUESTO_KEY) != tipo_repuesto:
                    st.session_state[PREVISION_ULTIMO_REPUESTO_KEY] = tipo_repuesto
                    st.session_state[PREVISION_DF_KEY] = df_sheet
                elif PREVISION_DF_KEY not in st.session_state:
                    st.session_state[PREVISION_DF_KEY] = df_sheet

                # -----------------------------------------------------

                df_data = df_sheet[PREVISION_COLS].copy()
                df_prevision = df_sheet[PREVISION_FORECAST_COLS].copy()

                df_data["Mes"] = df_data["Mes"].apply(self.arreglar_fechas)
                df_prevision["FechaPrevision"] = df_prevision["FechaPrevision"].apply(self.arreglar_fechas)

                df_data = df_data.dropna(subset=["Mes"])
                df_prevision = df_prevision.dropna(subset=["FechaPrevision"])

                # ------------------------------------------------
                if not df_data.empty and not df_prevision.empty:
                    figs, titulo = PrevisionPlotter(df_data, df_prevision, tipo_repuesto).create_plot()
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
            if st.toggle("Actualizar datos"):
                stock_col, consumo_col = st.columns((1,3))

                with stock_col:
                    df_modificado_stock = st.data_editor(
                        st.session_state[PREVISION_DF_KEY],
                        disabled=False,
                        num_rows="dynamic",
                        height=600,
                        key=PREVISION_STOCK_EDITOR_KEY,
                        column_order=PREVISION_STOCK_COLS,
                    )

                    _, centro_stock_guardar_col, _ = st.columns((1, 3, 0.5))

                    with centro_stock_guardar_col:
                        if st.button("💾 Guardar cambios de stock"):
                            google_sheet.save_and_update_forecast(
                                df_modificado=df_modificado_stock,
                                df_consumo=st.session_state[PREVISION_DF_KEY],
                                df_stock=df_modificado_stock,
                                tipo_repuesto=tipo_repuesto,
                                df_key=PREVISION_DF_KEY,
                                editor_key=PREVISION_STOCK_EDITOR_KEY,
                                celda_inicio="A2",
                                col_fin="B",
                                columnas_a_guardar=PREVISION_STOCK_COLS
                            )

                with consumo_col:
                    df_modificado_consumo = st.data_editor(
                        st.session_state[PREVISION_DF_KEY],
                        disabled=False,
                        num_rows="dynamic",
                        height=600,
                        key=PREVISION_EDITOR_KEY,
                        column_order=PREVISION_COLS,
                    )

                    _, centro_consumo_guardar_col, _ = st.columns((2.5, 3, 0.5))

                    with centro_consumo_guardar_col:
                        if st.button("💾 Guardar cambios de consumo"):
                            google_sheet.save_and_update_forecast(
                                df_modificado=df_modificado_consumo,
                                df_consumo=df_modificado_consumo,
                                df_stock=df_stock,
                                tipo_repuesto=tipo_repuesto,
                                df_key=PREVISION_DF_KEY,
                                editor_key=PREVISION_EDITOR_KEY,
                                celda_inicio="D2",
                                col_fin="G",
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