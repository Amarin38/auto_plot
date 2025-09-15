import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.forecast_plotter import ForecastPlotter
from src.utils.exception_utils import execute_safely


class ForecastPage:
    @execute_safely
    def prevision_options(self):
        plot = ForecastPlotter()

        col1, col2 = st.columns([1, 5], vertical_alignment="top", gap="small")


        with col1.container(height=100):
            opcion_prevision = self.add_selectbox()

        with col2.container(height=600):
            match (opcion_prevision):
                case "Inyectores": ...
                case "Bombas inyectoras": ...
                case "Bombas urea": ...
                case "Calipers": ...
                case "Camaras": ...
                case "DVRs": ...
                case "Electroválvulas 5 vias": ...
                case "Flotantes de gasoil": ...
                case "Herramientas": ...
                case "Retenes": 
                    figs = plot.create_plot("todo retenes", "RETEN")
                    st.subheader(plot._devolver_titulo("Retenes"))
                case "Sensores": ...
                case "Taladros": ...
            
            for fig in figs:
                st.plotly_chart(fig)
                
    
    def add_selectbox(self):
        return st.selectbox("Selecciona una previsión:", ["------", 
                                                          "Inyectores", "Bombas inyectoras", "Bombas urea", "Calipers", 
                                                          "Camaras", "DVRs", "Electroválvulas 5 vias", "Flotantes de gasoil", 
                                                          "Herramientas", "Retenes", "Sensores", "Taladros"])
    