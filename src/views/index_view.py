import sys, os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.index_plotter import  IndexPlotter
from src.utils.exception_utils import execute_safely

class IndexPage:
    @execute_safely
    def indice_options(self):
        plot = IndexPlotter()

        col1, col2 = st.columns([1, 5], vertical_alignment="top", gap="small")
        
        with col1.container(height=100):
            opcion_indice = self.add_selectbox()

        with col2.container(height=600):
            match(opcion_indice):
                case "Inyectores": 
                    figs = plot.create_plot("todos inyectores", "VEHICLE", "INYECTOR", "INYECTOR")
                    st.subheader(plot._devolver_titulo("Inyectores"))
                case "Bombas inyectoras": 
                    figs = plot.create_plot("todas bombas inyectoras", "VEHICLE", "BOMBA INYECTORA")
                    st.subheader(plot._devolver_titulo("Bombas Inyectoras"))
                case "Bombas urea": 
                    figs = plot.create_plot("todas bombas urea", "VEHICLE", "BOMBA UREA")
                    st.subheader(plot._devolver_titulo("Bombas de Urea"))
                case "Calipers": 
                    figs = plot.create_plot("todos calipers", "VEHICLE", "CALIPER")
                    st.subheader(plot._devolver_titulo("Calipers"))
                case "Camaras": 
                    figs = plot.create_plot("todas camaras", "VEHICLE", "CAMARA")
                    st.subheader(plot._devolver_titulo("Cámaras"))
                case "DVRs": 
                    figs = plot.create_plot("todos dvr", "VEHICLE", "DVR")
                    st.subheader(plot._devolver_titulo("DVR"))
                case "Electroválvulas 5 vias": 
                    figs = plot.create_plot("todas electrovalvulas", "VEHICLE", "ELECTROVALVULA")
                    st.subheader(plot._devolver_titulo("Electroválvulas"))
                case "Flotantes de gasoil": 
                    figs = plot.create_plot("todos flotantes gasoil", "VEHICLE", "FLOTANTE GASOIL")
                    st.subheader(plot._devolver_titulo("Flotantes gasoil"))
                case "Herramientas": 
                    figs = plot.create_plot("todas herramientas", "VEHICLE", "HERRAMIENTA")
                    st.subheader(plot._devolver_titulo("Herramientas"))
                case "Retenes": 
                    figs = plot.create_plot("todos retenes", "VEHICLE", "RETEN")
                    st.subheader(plot._devolver_titulo("Retenes"))
                case "Sensores": 
                    figs = plot.create_plot("todos sensores", "VEHICLE", "SENSOR")
                    st.subheader(plot._devolver_titulo("Sensores"))
                case "Taladros": 
                    figs = plot.create_plot("todos taladros", "VEHICLE", "TALADRO")
                    st.subheader(plot._devolver_titulo("Taladros"))

            for fig in figs:
                st.plotly_chart(fig) 


    def add_selectbox(self):
        return st.selectbox("Selecciona un índice:", ["------", 
                                                      "Inyectores", "Bombas inyectoras", "Bombas urea", "Calipers", 
                                                      "Camaras", "DVRs", "Electroválvulas 5 vias", "Flotantes de gasoil", 
                                                      "Herramientas", "Retenes", "Sensores", "Taladros"])


             