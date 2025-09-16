import sys, os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.config.constants import OPCIONES_REP_DB, OPCIONES_CARGAR_DATOS
from src.config.enums import IndexTypeEnum

from src.utils.exception_utils import execute_safely
from src.utils.common_utils import CommonUtils

from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner

from src.services.analysis.index import Index 
from src.services.analysis.maxmin import MaxMin
from src.services.analysis.deviation_trend import DeviationTrend
from src.services.analysis.forecast.forecast_with_zero import ForecastWithZero


class LoadDataSideBar:
    def __init__(self) -> None:
        self.common = CommonUtils()
        self.inventory = InventoryDataCleaner()
        self.expander_load = st.sidebar.expander("Cargar datos")


    @execute_safely
    def select_data(self):
        with self.expander_load:
            uploaded_files = st.file_uploader("Ingresa datos para actualizar", accept_multiple_files="directory")
            select_load = st.selectbox("Tabla", OPCIONES_CARGAR_DATOS)
            df = self.load_data(select_load, uploaded_files)

            if df is not None:
                match select_load:
                    case "Indices de consumo":
                        select_indice = st.selectbox("Indice", OPCIONES_REP_DB)
                        select_tipo = st.selectbox("Tipo", IndexTypeEnum)

                        load_button = st.button("Cargar datos", type="primary", use_container_width=True, 
                                                on_click=Index().calculate(df, select_indice, select_tipo))
                                
                    case "Prevision de connsumo":
                        select_prevision = st.selectbox("Prevision", OPCIONES_REP_DB)

                        load_button = st.button("Cargar datos", type="primary", use_container_width=True, 
                                                on_click=ForecastWithZero(df, select_prevision).create_forecast())
                        
                    case "Desviacion de indices":
                        load_button = st.button("Cargar datos", type="primary", use_container_width=True, 
                                                on_click=DeviationTrend().calcular_desviaciones_totales(df))
                        
                    case "Maximos y minimos":
                        mult_por = float(st.text_input("Multiplicar por: "))
                        load_button = st.button("Cargar datos", type="primary", use_container_width=True,
                                                on_click=MaxMin().calculate(df, mult_por))


    @execute_safely
    def load_data(self, select_load, uploaded_files):
        match select_load:
            case "Desviacion de indices":
                df = self.common.concat_dataframes(uploaded_files)
                print(df)
                return df
            case _:
                if uploaded_files is not None:
                    return self.inventory.run_all(uploaded_files) # junto todos los archivos
            
    
    