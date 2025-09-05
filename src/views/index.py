import sys, os
import streamlit as st
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plotting.auto_index_plotter import  AutoIndexPlotter

class IndexPage:
    def indice_options(self):
        opcion_indice = self.add_select_box()

        if opcion_indice != "------":
            st.title(f"Indice de {opcion_indice}")
        
        match(opcion_indice):
            case "Inyectores":
                self.add_barplot("inyectores", "todos inyectores", "vehicle", "INYECTOR", "INYECTOR")
            case "Bombas inyectoras":
                self.add_barplot("bombas inyectoras", "todas bombas inyectoras", "vehicle", "BOMBA INYECTORA")
            case "Bombas urea":
                self.add_barplot("bombas urea", "todas bombas urea", "vehicle", "BOMBA UREA")
            case "Calipers":
                self.add_barplot("calipers", "todos calipers", "vehicle", "CALIPER")
            case "Camaras":
                self.add_barplot("camaras", "todas camaras", "vehicle", "CAMARA")
            case "DVRs":
                self.add_barplot("dvr", "todos dvr", "vehicle", "DVR")
            case "Electroválvulas 5 vias":
                self.add_barplot("electrovalvulas", "todas electrovalvulas", "vehicle", "ELECTROVALVULA")
            case "Flotantes de gasoil":
                self.add_barplot("flotantes gasoil", "todos flotantes gasoil", "vehicle", "FLOTANTE GASOIL")
            case "Herramientas":
                self.add_barplot("herramientas", "todas herramientas", "vehicle", "HERRAMIENTA")
            case "Retenes":
                self.add_barplot("retenes", "todos retenes", "vehicle", "RETEN")
            case "Sensores":
                self.add_barplot("sensores", "todos sensores", "vehicle", "SENSOR")
            case "Taladros":
                self.add_barplot("taladros", "todos taladros", "vehicle", "TALADRO")


    def add_select_box(self):
        return st.selectbox("Indices de consumo: ", ["------", 
                                                     "Inyectores", "Bombas inyectoras", "Bombas urea", "Calipers", 
                                                     "Camaras", "DVRs", "Electroválvulas 5 vias", "Flotantes de gasoil", 
                                                     "Herramientas", "Retenes", "Sensores", "Taladros"])


    def add_barplot(self, file: str, directory: str, type_index: str, type_repuesto: str, filtro: Optional[str] = None):
        autoplot = AutoIndexPlotter(file, directory, type_index, type_repuesto, filtro)
        
        fecha = autoplot.devolver_fecha()
        st.subheader(f"Ultima actualizacion: {fecha}")

        figs = autoplot.create_plot()
        figs_len = int(len(figs)/2)

        figs1 = figs[figs_len:]
        figs2 = figs[:figs_len]

        col1, col2 = st.columns(2)

        with col1:
            for fig in figs1:
                st.plotly_chart(fig)

        with col2:
            for fig in figs2:
                st.plotly_chart(fig)
        