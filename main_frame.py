import streamlit as st

from infrastructure import CommonBase, ServicesBase
from infrastructure import common_engine, services_engine

from view.home import home
from view.prevision_consumo import prevision
from view.desviacion_indices import desviacion_indices
from view.maximos_minimos import maximos_minimos
from view.indices_consumo import indices_consumo
from view.cargar_datos import cargar_datos
from view.duracion_repuestos import duracion_repuestos
from view.falla_equipos_garantia import falla_equipos_garantias

from config.constants import (PAG_PRINCIPAL, PAG_CARGAR_DATOS, PAG_INDICES, PAG_PREVISION,
                              PAG_DESVIACION_INDICES, PAG_FALLA_GARANTIAS, PAG_maximos_minimos, PAG_DURACION)

# Services DB -----------------------------------------------------------------------------------
from infrastructure.db.models.services_model.desviacion_indices_model import  DesviacionIndicesModel
from infrastructure.db.models.services_model.maximos_minimos_model import MaximosMinimosModel
from infrastructure.db.models.services_model.consumo_garantias_model import ConsumoGarantiasModel
from infrastructure.db.models.services_model.prevision_model import PrevisionModel
from infrastructure.db.models.services_model.prevision_data_model import PrevisionDataModel
from infrastructure.db.models.services_model.falla_garantias_model import FallaGarantiasModel
from infrastructure.db.models.services_model.indice_consumo_model import IndiceConsumoModel
from infrastructure.db.models.services_model.duracion_repuestos_model import DuracionRepuestosModel
from infrastructure.db.models.services_model.distribucion_normal_model import DistribucionNormalModel

# Common DB -----------------------------------------------------------------------------------
from infrastructure.db.models.common_model.coches_cabecera_model import CochesCabeceraModel
from infrastructure.db.models.common_model.datos_garantias_model import DatosGarantiasModel
from infrastructure.db.models.common_model.json_config_model import JSONConfigModel

# -----------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Estadisticas Dota",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

view = {
    "Inicio":[
        st.Page(home, title=PAG_PRINCIPAL),
        st.Page(cargar_datos, title=PAG_CARGAR_DATOS)
    ],
    "Estadísticas":[
        st.Page(indices_consumo, title=PAG_INDICES),
        st.Page(prevision, title=PAG_PREVISION),
        st.Page(desviacion_indices, title=PAG_DESVIACION_INDICES),
        st.Page(duracion_repuestos, title=PAG_DURACION),
        st.Page(falla_equipos_garantias, title=PAG_FALLA_GARANTIAS),
        st.Page(maximos_minimos, title=PAG_maximos_minimos)
    ]
}

nav = st.navigation(view, position="top")

if __name__ == "__main__":
    CommonBase.metadata.create_all(common_engine)
    ServicesBase.metadata.create_all(services_engine)

    nav.run()
