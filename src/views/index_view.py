import sys, os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.index_plotter import  IndexPlotter

from src.utils.exception_utils import execute_safely

from src.config.constants import REPUESTOS_OPT, SELECT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS
from src.config.enums import IndexTypeEnum


class IndexPage:
    def __init__(self) -> None:
        self.plot = IndexPlotter()


    @execute_safely
    def indice_options(self) -> None:
        figs = None
        col1, col2 = st.columns(DISTANCE_COLS)
        
        with col1.container(height=SELECT_BOX_HEIGHT):
            opcion_indice = st.selectbox("Selecciona un índice:", REPUESTOS_OPT)

            if opcion_indice != REPUESTOS_OPT[0]:
                with col1.container(height=SELECT_BOX_HEIGHT):
                    opcion_tipo_indice = st.selectbox("Selecciona un tipo de indice:", IndexTypeEnum) # TODO: implementar el tipo de indice para el cálculo
                    
                match opcion_indice:
                        case "Inyectores": figs = self.plot.create_plot(opcion_tipo_indice, "INYECTOR", "INYECTOR")
                        case "Bombas inyectoras": figs = self.plot.create_plot(opcion_tipo_indice, "BOMBA INYECTORA")
                        case "Bombas urea": figs = self.plot.create_plot(opcion_tipo_indice, "BOMBA UREA")
                        case "Calipers": figs = self.plot.create_plot(opcion_tipo_indice, "CALIPER")
                        case "Camaras": figs = self.plot.create_plot(opcion_tipo_indice, "CAMARA")
                        case "DVRs": figs = self.plot.create_plot(opcion_tipo_indice, "DVR")
                        case "Electroválvulas 5 vias": figs = self.plot.create_plot(opcion_tipo_indice, "ELECTROVALVULA")
                        case "Flotantes de gasoil": figs = self.plot.create_plot(opcion_tipo_indice, "FLOTANTE GASOIL")
                        case "Herramientas": figs = self.plot.create_plot(opcion_tipo_indice, "HERRAMIENTA")
                        case "Retenes": figs = self.plot.create_plot(opcion_tipo_indice, "RETEN")
                        case "Sensores": figs = self.plot.create_plot(opcion_tipo_indice, "SENSOR")
                        case "Taladros": figs = self.plot.create_plot(opcion_tipo_indice, "TALADRO")
        

        with col2.container(height=PLOT_BOX_HEIGHT):
            if opcion_indice != REPUESTOS_OPT[0]:
                st.subheader(self.plot._devolver_titulo(opcion_indice))

            if figs is not None:
                for fig in figs:
                    st.plotly_chart(fig) 
            

        

             