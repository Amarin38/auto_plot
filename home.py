import streamlit as st

from infrastructure import DBBase, db_engine
from presentation.main_page import main
from presentation.prevision_consumo_page import prevision
from presentation.desviacion_indices_page import desviacion_indices
from presentation.maximos_minimos_page import maximos_minimos
from presentation.indices_consumo_page import indices_consumo
from presentation.cargar_datos_page import cargar_datos
from presentation.duracion_repuestos_page import duracion_repuestos
from presentation.falla_equipos_garantia_page import falla_equipos_garantias
from presentation.transferencias_entre_depositos_page import transferencias_entre_depositos

from config.constants import (PAG_PRINCIPAL, PAG_CARGAR_DATOS, PAG_INDICES, PAG_PREVISION,
                              PAG_DESVIACION_INDICES, PAG_FALLA_GARANTIAS, PAG_MAXIMOS_MINIMOS, PAG_DURACION,
                              PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)

# Services DB -----------------------------------------------------------------------------------

# Common DB -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Estadisticas Dota",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

pages = {
    "Inicio":[
        st.Page(main, title=PAG_PRINCIPAL),
        st.Page(cargar_datos, title=PAG_CARGAR_DATOS)
    ],
    "Estadísticas generales":[
        st.Page(indices_consumo, title=PAG_INDICES),
        st.Page(prevision, title=PAG_PREVISION),
        st.Page(desviacion_indices, title=PAG_DESVIACION_INDICES),
        st.Page(duracion_repuestos, title=PAG_DURACION),
        st.Page(falla_equipos_garantias, title=PAG_FALLA_GARANTIAS),
        st.Page(maximos_minimos, title=PAG_MAXIMOS_MINIMOS)
    ],
    "Estadísticas gomería":[
        st.Page(transferencias_entre_depositos, title=PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)
    ]
}

nav = st.navigation(pages, position="top")

if __name__ == "__main__":
    # DBBase.metadata.create_all(db_engine)
    # DBBase.metadata.create_all(db_engine)
    DBBase.metadata.create_all(db_engine)
    nav.run()
