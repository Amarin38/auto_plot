import sys, os
import streamlit as st
from typing import Optional, Literal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plotting.auto_index_plotter import  AutoIndexPlotter
from src.views.streamlit_utils import StreamlitUtils

class IndexPage:
    def indice_options(self):
        self.opcion_indice = self.add_select_box()
        
        match(self.opcion_indice):
            case "Inyectores": self.add_barplot("todos inyectores", "VEHICLE", "INYECTOR", "INYECTOR")
            case "Bombas inyectoras": self.add_barplot("todas bombas inyectoras", "VEHICLE", "BOMBA INYECTORA")
            case "Bombas urea": self.add_barplot("todas bombas urea", "VEHICLE", "BOMBA UREA")
            case "Calipers": self.add_barplot("todos calipers", "VEHICLE", "CALIPER")
            case "Camaras": self.add_barplot("todas camaras", "VEHICLE", "CAMARA")
            case "DVRs": self.add_barplot("todos dvr", "VEHICLE", "DVR")
            case "Electroválvulas 5 vias": self.add_barplot("todas electrovalvulas", "VEHICLE", "ELECTROVALVULA")
            case "Flotantes de gasoil": self.add_barplot("todos flotantes gasoil", "VEHICLE", "FLOTANTE GASOIL")
            case "Herramientas": self.add_barplot("todas herramientas", "VEHICLE", "HERRAMIENTA")
            case "Retenes": self.add_barplot("todos retenes", "VEHICLE", "RETEN")
            case "Sensores": self.add_barplot("todos sensores", "VEHICLE", "SENSOR")
            case "Taladros": self.add_barplot("todos taladros", "VEHICLE", "TALADRO")

    def add_select_box(self):
        return st.selectbox("Selecciona un índice:", ["------", 
                                                      "Inyectores", "Bombas inyectoras", "Bombas urea", "Calipers", 
                                                      "Camaras", "DVRs", "Electroválvulas 5 vias", "Flotantes de gasoil", 
                                                      "Herramientas", "Retenes", "Sensores", "Taladros"])


    def add_barplot(self, directory: str, type_index: Literal["MOTOR", "VEHICLE"], type_repuesto: str, filtro: Optional[str] = None):
        autoplot = AutoIndexPlotter(directory, type_index, type_repuesto, filtro)
        StreamlitUtils().show_plot(autoplot, self.opcion_indice)
        