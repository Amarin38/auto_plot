import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plotting.auto_forecast_plotter import AutoForecastPlotter
from src.views.streamlit_utils import StreamlitUtils
from src.services.utils.exception_utils import execute_safely


class ForecastPage:
    def tendencia_options(self):
        opcion_tendencia = self.selectbox()
        if opcion_tendencia != "------":
            st.title(f"Tendencia de {opcion_tendencia} a 12 meses")


        match (opcion_tendencia):
            case "Inyectores":
                ...
            case "Bombas inyectoras":
                ...                
            case "Bombas urea":
                ...
            case "Calipers":
                ...
            case "Camaras":
                ...
            case "DVRs":
                ...
            case "Electroválvulas 5 vias":
                ...
            case "Flotantes de gasoil":
                ...
            case "Herramientas":
                ...
            case "Retenes":
                self.add_barplot("todo retenes", "RETEN")
            case "Sensores":
                ...
            case "Taladros":
                ...

    
    def selectbox(self):
        return st.selectbox("Tendencias de consumo: ", ["------", 
                                                     "Inyectores", "Bombas inyectoras", "Bombas urea", "Calipers", 
                                                     "Camaras", "DVRs", "Electroválvulas 5 vias", "Flotantes de gasoil", 
                                                     "Herramientas", "Retenes", "Sensores", "Taladros"])
    

    @execute_safely
    def add_barplot(self, directory: str, type: str):
        autoplot = AutoForecastPlotter(directory, type)
        StreamlitUtils().show_plot(autoplot)
        