import streamlit as st

from infrastructure import CommonBase, ServicesBase
from infrastructure import common_engine, services_engine

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
from infrastructure.db.models.services.desviacion_indices_model import  DesviacionIndicesModel
from infrastructure.db.models.services.maximos_minimos_model import MaximosMinimosModel
from infrastructure.db.models.services.consumo_garantias_model import ConsumoGarantiasModel
from infrastructure.db.models.services.prevision_model import PrevisionModel
from infrastructure.db.models.services.prevision_data_model import PrevisionDataModel
from infrastructure.db.models.services.falla_garantias_model import FallaGarantiasModel
from infrastructure.db.models.services.indice_consumo_model import IndiceConsumoModel
from infrastructure.db.models.services.duracion_repuestos_model import DuracionRepuestosModel
from infrastructure.db.models.services.distribucion_normal_model import DistribucionNormalModel
from infrastructure.db.models.services.transferencias_entre_depositos_model import TransferenciasEntreDepositosModel
from infrastructure.db.models.services.diferencia_movimientos_entre_depositos_model import DiferenciaMovimientosEntreDepositosModel

# Common DB -----------------------------------------------------------------------------------
from infrastructure.db.models.common.coches_cabecera_model import CochesCabeceraModel
from infrastructure.db.models.common.datos_garantias_model import DatosGarantiasModel
from infrastructure.db.models.common.json_config_model import JSONConfigModel

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
    CommonBase.metadata.create_all(common_engine)
    ServicesBase.metadata.create_all(services_engine)

    nav.run()
