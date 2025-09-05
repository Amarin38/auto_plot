import streamlit as st
from datetime import datetime

class ForecastPage:
    def __init__(self) -> None:
        self.date = datetime.today().strftime("%d-%m-%Y")

    
    def tendencia_options(self):
        opcion_tendencia = self.selectbox()
        if opcion_tendencia != "------":
            st.title(f"Tendencia de {opcion_tendencia} {self.date}")
            st.write(f"Se seleccionó {opcion_tendencia}") 


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
                ...
            case "Sensores":
                ...
            case "Taladros":
                ...

    def selectbox(self):
        return st.selectbox("Tendencias de compra: ", ["------", "Inyectores", "Bombas inyectoras", "Bombas urea"])