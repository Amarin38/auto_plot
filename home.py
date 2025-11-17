import streamlit as st

from infrastructure import DBBase, db_engine
from presentation.consumo_obligatorio_page import consumo_obligatorio
from presentation.main_page import main
from presentation.prevision_consumo_page import prevision
from presentation.desviacion_indices_page import desviacion_indices
from presentation.maximos_minimos_page import maximos_minimos
from presentation.indice_consumo_page import indice_consumo
from presentation.cargar_datos_page import cargar_datos
from presentation.duracion_repuestos_page import duracion_repuestos
from presentation.falla_equipos_garantia_page import falla_equipos_garantias
from presentation.transferencias_depositos_page import transferencias_entre_depositos
from presentation.historial_consumo_page import historial_consumo

from config.constants import (PAG_PRINCIPAL, PAG_CARGAR_DATOS, PAG_INDICES, PAG_PREVISION,
                              PAG_DESVIACION_INDICES, PAG_FALLA_GARANTIAS, PAG_MAXIMOS_MINIMOS, PAG_DURACION,
                              PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, PAG_HISTORIAL, PAG_CONSUMO_OBLIGATORIO)

from infrastructure.db.models.coches_cabecera_model import CochesCabeceraModel
from infrastructure.db.models.consumo_garantias_model import ConsumoGarantiasModel
from infrastructure.db.models.datos_garantias_model import DatosGarantiasModel
from infrastructure.db.models.desviacion_indices_model import DesviacionIndicesModel
from infrastructure.db.models.diferencia_mov_dep_model import DiferenciaMovimientosEntreDepositosModel
from infrastructure.db.models.distribucion_normal_model import DistribucionNormalModel
from infrastructure.db.models.duracion_repuestos_model import DuracionRepuestosModel
from infrastructure.db.models.falla_garantias_model import FallaGarantiasModel
from infrastructure.db.models.indice_consumo_model import IndiceConsumoModel
from infrastructure.db.models.json_config_model import JSONConfigModel
from infrastructure.db.models.maximos_minimos_model import MaximosMinimosModel
from infrastructure.db.models.prevision_data_model import PrevisionDataModel
from infrastructure.db.models.prevision_model import PrevisionModel
from infrastructure.db.models.transferencias_dep_model import TransferenciasEntreDepositosModel

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
        st.Page(indice_consumo, title=PAG_INDICES),
        st.Page(historial_consumo, title=PAG_HISTORIAL),
        st.Page(consumo_obligatorio, title=PAG_CONSUMO_OBLIGATORIO),
        st.Page(prevision, title=PAG_PREVISION),
        st.Page(desviacion_indices, title=PAG_DESVIACION_INDICES),
        st.Page(duracion_repuestos, title=PAG_DURACION),
        st.Page(maximos_minimos, title=PAG_MAXIMOS_MINIMOS)
    ],
    "Estadísticas garantías":[
        st.Page(falla_equipos_garantias, title=PAG_FALLA_GARANTIAS),
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
