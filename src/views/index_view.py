import sys, os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.index_plotter import  IndexPlotter
from src.utils.exception_utils import execute_safely
from src.config.constants import OPCIONES_REP, OPCIONES_TIPOS_INDICES, SELECT_BOX_HEIGHT

class IndexPage:
    @execute_safely
    def indice_options(self) -> None:
        figs = None
        plot = IndexPlotter()

        col1, col2 = st.columns([1, 5], vertical_alignment="top", gap="small")
        
        with col1.container(height=SELECT_BOX_HEIGHT):
            opcion_indice = st.selectbox("Selecciona un índice:", OPCIONES_REP)

            if opcion_indice != OPCIONES_REP[0]:
                with col1.container(height=SELECT_BOX_HEIGHT):
                    opcion_tipo_indice = st.selectbox("Selecciona un tipo de indice:", OPCIONES_TIPOS_INDICES) # TODO: implementar el tipo de indice para el cálculo
                    
                match opcion_indice:
                        case "Inyectores": figs = plot.create_plot("VEHICLE", "INYECTOR", "INYECTOR")
                        case "Bombas inyectoras": figs = plot.create_plot("VEHICLE", "BOMBA INYECTORA")
                        case "Bombas urea": figs = plot.create_plot("VEHICLE", "BOMBA UREA")
                        case "Calipers": figs = plot.create_plot("VEHICLE", "CALIPER")
                        case "Camaras": figs = plot.create_plot("VEHICLE", "CAMARA")
                        case "DVRs": figs = plot.create_plot("VEHICLE", "DVR")
                        case "Electroválvulas 5 vias": figs = plot.create_plot("VEHICLE", "ELECTROVALVULA")
                        case "Flotantes de gasoil": figs = plot.create_plot("VEHICLE", "FLOTANTE GASOIL")
                        case "Herramientas": figs = plot.create_plot("VEHICLE", "HERRAMIENTA")
                        case "Retenes": figs = plot.create_plot("VEHICLE", "RETEN")
                        case "Sensores": figs = plot.create_plot("VEHICLE", "SENSOR")
                        case "Taladros": figs = plot.create_plot("VEHICLE", "TALADRO")
        

        with col2.container(height=600):
            if opcion_indice != OPCIONES_REP[0]:
                st.subheader(plot._devolver_titulo(opcion_indice))

            if figs is not None:
                for fig in figs:
                    st.plotly_chart(fig) 
            

        

             