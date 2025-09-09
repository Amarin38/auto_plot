import sys, os
import streamlit as st
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plotting.auto_index_plotter import  AutoIndexPlotter
from src.views.streamlit_utils import StreamlitUtils

class IndexPage:
    def indice_options(self):
        opcion_indice = self.add_select_box()

        if opcion_indice != "------":
            st.title(f"Indice de {opcion_indice}")
        
        match(opcion_indice):
            case "Inyectores":
                self.add_barplot("todos inyectores", "vehicle", "INYECTOR", "INYECTOR")
            case "Bombas inyectoras":
                self.add_barplot("todas bombas inyectoras", "vehicle", "BOMBA INYECTORA")
            case "Bombas urea":
                self.add_barplot("todas bombas urea", "vehicle", "BOMBA UREA")
            case "Calipers":
                self.add_barplot("todos calipers", "vehicle", "CALIPER")
            case "Camaras":
                self.add_barplot("todas camaras", "vehicle", "CAMARA")
            case "DVRs":
                self.add_barplot("todos dvr", "vehicle", "DVR")
            case "Electroválvulas 5 vias":
                self.add_barplot("todas electrovalvulas", "vehicle", "ELECTROVALVULA")
            case "Flotantes de gasoil":
                self.add_barplot("todos flotantes gasoil", "vehicle", "FLOTANTE GASOIL")
            case "Herramientas":
                self.add_barplot("todas herramientas", "vehicle", "HERRAMIENTA")
            case "Retenes":
                self.add_barplot("todos retenes", "vehicle", "RETEN")
            case "Sensores":
                self.add_barplot("todos sensores", "vehicle", "SENSOR")
            case "Taladros":
                self.add_barplot("todos taladros", "vehicle", "TALADRO")


    def add_select_box(self):
        return st.selectbox("Indices de consumo: ", ["------", 
                                                     "Inyectores", "Bombas inyectoras", "Bombas urea", "Calipers", 
                                                     "Camaras", "DVRs", "Electroválvulas 5 vias", "Flotantes de gasoil", 
                                                     "Herramientas", "Retenes", "Sensores", "Taladros"])


    def add_barplot(self, directory: str, type_index: str, type_repuesto: str, filtro: Optional[str] = None):

        autoplot = AutoIndexPlotter(directory, type_index, type_repuesto, filtro)
        StreamlitUtils().show_plot(autoplot)
        