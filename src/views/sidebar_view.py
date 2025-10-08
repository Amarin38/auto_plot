import sys, os
import streamlit as st

from src.config.constants import PLACEHOLDER
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
            select_load = st.selectbox("Selecciona la tabla a ingresar: ", LoadDataEnum, index=None, placeholder=PLACEHOLDER)

            if select_load and len(uploaded_files) > 0:
                match select_load:
                    case LoadDataEnum.INDICES_DE_CONSUMO:
                        select_repuesto = st.selectbox("Selecciona un repuesto: ", RepuestoEnum, index=None, placeholder=PLACEHOLDER)
                        select_tipo = st.selectbox("Selecciona un tipo de indice: ", IndexTypeEnum, index=None, placeholder=PLACEHOLDER)

                        if select_repuesto and select_tipo:
                            df = self.load_data(select_load, uploaded_files)
                            self.load_data_bttn(lambda: Index().calculate(df, select_repuesto.upper(), select_tipo.upper()))

                    case LoadDataEnum.PREVISION_DE_CONSUMO:
                        select_prevision = st.selectbox("Selecciona el tipo de prevision: ", RepuestoEnum, index=None, placeholder=PLACEHOLDER)

                        if select_prevision:
                            df = self.load_data(select_load, uploaded_files)
                            self.load_data_bttn(lambda: create_forecast(df, select_prevision.upper()))

                    case LoadDataEnum.DESVIACION_DE_INDICES:
                        df = self.load_data(select_load, uploaded_files)
                        self.load_data_bttn(lambda: DeviationTrend().calculate(df))

                    case LoadDataEnum.FALLA_GARANTIAS:
                        df = self.load_data(select_load, uploaded_files)
                        self.load_data_bttn(lambda: calcular_falla_garantias(df))

                    case LoadDataEnum.DATOS_GARANTIAS:
                        df = self.load_data(select_load, uploaded_files)
                        self.load_data_bttn(lambda: guardar_datos_garantias(df))

                    case LoadDataEnum.CONSUMO_GARANTIAS:
                        df = self.load_data(select_load, uploaded_files)
                        self.load_data_bttn(lambda: calcular_consumo_garantias(df))

                    case LoadDataEnum.MAXMIMOS_Y_MINIMOS:
                        mult_por = float(st.text_input("Multiplicar por: "))

                        if mult_por:
                            df = self.load_data(select_load, uploaded_files)
                            self.load_data_bttn(lambda: MaxMin().calculate(df, mult_por))
                        

    @execute_safely
    def load_data(self, select_load, uploaded_files):
        match select_load:
            case LoadDataEnum.DESVIACION_DE_INDICES | LoadDataEnum.FALLA_GARANTIAS | LoadDataEnum.CONSUMO_GARANTIAS | LoadDataEnum.DATOS_GARANTIAS:
                return self.common.concat_dataframes(uploaded_files)
            case _:
                if uploaded_files and select_load:
                    return self.inventory.run_all(uploaded_files)
                return None


    @staticmethod
    def load_data_bttn(func):
        st.button(
            label="Cargar datos",
            type="primary",
            use_container_width=True,
            on_click=func
        )
    