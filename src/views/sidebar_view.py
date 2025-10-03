import sys, os
import streamlit as st

from src.services.analysis.garantias import calcular_falla_garantias, calcular_consumo_garantias, \
    guardar_datos_garantias

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.config.enums import IndexTypeEnum, RepuestoEnum, LoadDataEnum

from src.utils.exception_utils import execute_safely
from src.utils.common_utils import CommonUtils

from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner

from src.services.analysis.index import Index 
from src.services.analysis.maxmin import MaxMin
from src.services.analysis.deviation_trend import DeviationTrend

from src.services.analysis.forecast import create_forecast


class LoadDataSideBar:
    def __init__(self) -> None:
        self.common = CommonUtils()
        self.inventory = InventoryDataCleaner()
        self.expander_load = st.sidebar.expander("Cargar datos")


    @execute_safely
    def select_data(self):
        with self.expander_load:
            uploaded_files = st.file_uploader("Ingresa datos para actualizar", accept_multiple_files="directory")
            select_load = st.selectbox("Tabla", LoadDataEnum, index=None, placeholder="------")

            df = self.load_data(select_load, uploaded_files)
            
            if df is not None:
                match select_load:
                    case LoadDataEnum.INDICES_DE_CONSUMO:
                        select_indice = st.selectbox("Indice", RepuestoEnum, index=None, placeholder="------")
                        select_tipo = st.selectbox("Tipo", IndexTypeEnum, index=None, placeholder="------")

                        self.load_data_bttn(lambda: Index().calculate(df, select_indice, select_tipo))

                    case LoadDataEnum.PREVISION_DE_CONSUMO:
                        select_prevision = st.selectbox("Prevision", RepuestoEnum, index=None, placeholder="------")
                        self.load_data_bttn(lambda: create_forecast(df, select_prevision))

                    case LoadDataEnum.DESVIACION_DE_INDICES:
                        self.load_data_bttn(lambda: DeviationTrend().calculate(df))

                    case LoadDataEnum.FALLA_GARANTIAS:
                        self.load_data_bttn(lambda: calcular_falla_garantias(df))

                    case LoadDataEnum.DATOS_GARANTIAS:
                        self.load_data_bttn(lambda: guardar_datos_garantias(df))

                    case LoadDataEnum.CONSUMO_GARANTIAS:
                        self.load_data_bttn(lambda: calcular_consumo_garantias(df))

                    case LoadDataEnum.MAXMIMOS_Y_MINIMOS:
                        mult_por = float(st.text_input("Multiplicar por: "))
                        self.load_data_bttn(lambda: MaxMin().calculate(df, mult_por))
                        

    @execute_safely
    def load_data(self, select_load, uploaded_files):
        match select_load:
            case "Desviacion de indices":
                df = self.common.concat_dataframes(uploaded_files)
                return df
            case _:
                if uploaded_files is not None:
                    return self.inventory.run_all(uploaded_files) # junto todos los archivos
                return None

    @staticmethod
    def load_data_bttn(func):
        st.button(
            label="Cargar datos",
            type="primary",
            use_container_width=True,
            on_click=func
        )
    