import sys, os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.config.constants import OPCIONES_REP_DB, OPCIONES_CARGAR_DATOS
from src.config.enums import IndexTypeEnum

from src.utils.exception_utils import execute_safely
from src.utils.common_utils import CommonUtils

from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner

from src.services.analysis.deviation_trend import DeviationTrend
from src.services.analysis.consumption_index.index import Index 
from src.services.analysis.forecast.forecast_with_zero import ForecastWithZero


class LoadDataSideBar:
    def __init__(self) -> None:
        self.inventory = InventoryDataCleaner()
        self.common = CommonUtils()
        self.expander_load = st.sidebar.expander("Cargar datos")

    @execute_safely
    def select_data(self):
        with self.expander_load:
            self.uploaded_files = st.file_uploader("Ingresa datos para actualizar", accept_multiple_files="directory")
            self.select_load = st.selectbox("Tabla", OPCIONES_CARGAR_DATOS)
            df = self.load_data()

            match self.select_load:
                case "Indices de consumo":
                    select_indice = st.selectbox("Indice", OPCIONES_REP_DB)
                    select_tipo = st.selectbox("Tipo", IndexTypeEnum)

                    match select_tipo:
                        case IndexTypeEnum.VEHICLE:
                            load_button = st.button("Cargar datos", type="primary", use_container_width=True, 
                                                    on_click=Index().calculate_by_vehicle(df, select_indice)) # type: ignore
                        case IndexTypeEnum.MOTOR:
                            load_button = st.button("Cargar datos", type="primary", use_container_width=True, 
                                                    on_click=Index().calculate_by_motor(df, select_indice)) # type: ignore
                            
                case "Prevision de connsumo":
                    select_prevision = st.selectbox("Prevision", OPCIONES_REP_DB)
                    load_button = st.button("Cargar datos", type="primary", use_container_width=True, 
                                            on_click=ForecastWithZero(df, select_prevision)) # type: ignore
                    
                case "Desviacion de indices":
                    load_button = st.button("Cargar datos", type="primary", use_container_width=True, 
                                            on_click=DeviationTrend().calcular_desviaciones_totales(df)) 


    @execute_safely
    def load_data(self):
        match self.select_load:
            case "Desviacion de indices":
                df = self.common.concat_dataframes(self.uploaded_files)
                print(df)
                return df
            case _:
                if self.uploaded_files is not None:
                    return self.inventory.run_all(self.uploaded_files)
            
    
    