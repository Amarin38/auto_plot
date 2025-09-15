import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.forecast_plotter import ForecastPlotter
from src.utils.exception_utils import execute_safely
from src.config.constants import OPCIONES_REP, SELECT_BOX_HEIGHT

class ForecastPage:
    @execute_safely
    def prevision_options(self):
        figs = None
        plot = ForecastPlotter()

        col1, col2 = st.columns([1, 5], vertical_alignment="top", gap="small")


        with col1.container(height=100):
            opcion_prevision = st.selectbox("Selecciona una previsión:", OPCIONES_REP)

            match opcion_prevision:
                case "Inyectores": ...
                case "Bombas inyectoras": ...
                case "Bombas urea": ...
                case "Calipers": ...
                case "Camaras": ...
                case "DVRs": ...
                case "Electroválvulas 5 vias": ...
                case "Flotantes de gasoil": ...
                case "Herramientas": ...
                case "Retenes": figs = plot.create_plot("RETEN")
                case "Sensores": ...
                case "Taladros": ...
             
        with col2.container(height=600):
            if opcion_prevision != OPCIONES_REP[0]:
                st.subheader(plot._devolver_titulo(opcion_prevision))
            
            if figs is not None:
                for fig in figs:
                    st.plotly_chart(fig)

    