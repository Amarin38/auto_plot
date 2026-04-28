import pandas as pd
import streamlit as st

from config.constants_common import PAGE_STRFTIME_DMY, FILE_STRFTIME_YMD
from domain.services.compute_consumo_prevision import create_forecast_gs
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from presentation.streamlit_components import SelectBoxComponents, OtherComponents, GoogleSheetsComponents
from utils.exception_utils import execute_safely
from viewmodels.consumo.prevision.data_vm import PrevisionDataVM

from viewmodels.consumo.prevision.plotter import PrevisionPlotter

from config.constants_views import (PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE, DISTANCE_COLS_SELECTBIGGER_PLOT,
                                    PAG_PREVISION, PREVISION_DF_KEY, PREVISION_SHEET_URL, PREVISION_COLS,
                                    PREVISION_EDITOR_KEY, PREVISION_FORECAST_COLS,
                                    PREVISION_REPUESTO_KEY, PREVISION_ULTIMO_REPUESTO_KEY, INDEX)
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

        aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
        config_col, graficos_col = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

        tipo_repuesto = self.select.select_box_tipo_repuesto(config_col, PREVISION_REPUESTO_KEY)

        if tipo_repuesto:
            google_sheet = GoogleSheetsComponents(PREVISION_SHEET_URL, tipo_repuesto, PREVISION_COLS)

            df_sheet = google_sheet.connect()
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

            with config_col:
                df_data = df_sheet[PREVISION_COLS].copy()
                df_prevision = df_sheet[PREVISION_FORECAST_COLS].copy()

                def arreglar_fechas_rebeldes(fecha):
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

                df_data["Mes"] = df_data["Mes"].apply(arreglar_fechas_rebeldes)
                df_prevision["FechaPrevision"] = df_prevision["FechaPrevision"].apply(arreglar_fechas_rebeldes)

                df_data = df_data.dropna(subset=["Mes"])
                df_prevision = df_prevision.dropna(subset=["FechaPrevision"])

                # ------------------------------------------------
                if not df_data.empty and not df_prevision.empty:
                    figs, titulo = PrevisionPlotter(df_data, df_prevision, tipo_repuesto).create_plot()
                    self.other.centered_title(titulo_col, titulo)

                    with graficos_col:
                        for fig in figs:
                            with st.container(height=PLOT_BOX_HEIGHT):
                                st.plotly_chart(fig)
                else:
                    self.other.mensaje_falta_rep(graficos_col)

                if st.toggle("Actualizar datos"):
                    df_modificado = st.data_editor(
                        st.session_state[PREVISION_DF_KEY],
                        disabled=False,
                        num_rows="dynamic",
                        height=600,
                        key=PREVISION_EDITOR_KEY,
                        column_order=PREVISION_COLS,
                    )

                    if st.button("💾 Guardar cambios de consumo"):
                        google_sheet.save_button_granular(df_modificado, df_key=PREVISION_DF_KEY, editor_key=PREVISION_EDITOR_KEY)

                    if st.button("Actualizar Google sheet"):
                        self.save_forecast_to_sheets(df_modificado, df_stock, tipo_repuesto, google_sheet)


    @staticmethod
    def save_forecast_to_sheets(df_sheet: pd.DataFrame, df_stock: pd.DataFrame, tipo_repuesto, gs) -> None:
        with st.spinner("Calculando pronósticos y subiendo a la nube..."):
            df_prevision = create_forecast_gs(df_sheet, df_stock, tipo_repuesto)

            if df_prevision is not None:
                gs.update_range_with_df(
                    df=df_prevision,
                    celda_inicial='I2',
                    rango_tabla='I2:M'
                )

                st.toast(f"Datos de {tipo_repuesto} sincronizados correctamente", icon="✅")
                st.cache_data.clear()

                if PREVISION_DF_KEY in st.session_state:
                    del st.session_state[PREVISION_DF_KEY]

                st.rerun()
            else:
                st.error("No se pudieron calcular las previsiones (revisa si hay datos suficientes).")