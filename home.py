import streamlit as st

from infrastructure import DBBase, db_engine
from presentation.dota_licitaciones_page import dota_licitaciones_page

from presentation.main_page import main
from presentation.cargar_datos_page import cargar_datos
from presentation.coches_cabecera_page import coches_cabecera
from presentation.consumo_obligatorio_page import consumo_obligatorio
from presentation.consumo_prevision_page import consumo_prevision
from presentation.consumo_indice_page import consumo_indice
from presentation.consumo_historial_page import consumo_historial
from presentation.garantias_falla_equipos_page import garantias_falla_equipos
from presentation.gomeria_transferencias_depositos_page import gomeria_transferencias_entre_depositos
from presentation.maximos_minimos_page import maximos_minimos
from presentation.duracion_repuestos_page import duracion_repuestos
from presentation.parque_movil_page import parque_movil
from presentation.sisssa_page import sissa_page

from config.constants_views import (PAG_PRINCIPAL, PAG_CARGAR_DATOS, PAG_INDICES, PAG_PREVISION,
                                    PAG_FALLA_GARANTIAS, PAG_MAXIMOS_MINIMOS, PAG_DURACION,
                                    PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, PAG_HISTORIAL, PAG_CONSUMO_OBLIGATORIO,
                                    PAG_COCHES_CABECERA, PAG_PARQUE_MOVIL, PAG_SISSSA, PAG_DOTA_LICITACIONES)

from infrastructure.db.models.coches_cabecera_model import CochesCabeceraModel
from infrastructure.db.models.garantias_consumo_model import GarantiasConsumoModel
from infrastructure.db.models.garantias_datos_model import GarantiasDatosModel
from infrastructure.db.models.garantias_falla_model import GarantiasFallaModel
from infrastructure.db.models.consumo_indice_model import ConsumoIndiceModel
from infrastructure.db.models.consumo_historial_model import ConsumoHistorialModel
from infrastructure.db.models.consumo_obligatorio_model import ConsumoObligatorioModel
from infrastructure.db.models.consumo_prevision_data_model import ConsumoPrevisionDataModel
from infrastructure.db.models.consumo_prevision_model import ConsumoPrevisionModel
from infrastructure.db.models.consumo_desviacion_indices_model import ConsumoDesviacionIndicesModel
from infrastructure.db.models.gomeria_diferencia_mov_dep_model import GomeriaDiferenciaMovEntreDepModel
from infrastructure.db.models.gomeria_transferencias_dep_model import GomeriaTransferenciasEntreDepModel
from infrastructure.db.models.distribucion_normal_model import DistribucionNormalModel
from infrastructure.db.models.duracion_repuestos_model import DuracionRepuestosModel
from infrastructure.db.models.maximos_minimos_model import MaximosMinimosModel
from infrastructure.db.models.json_config_model import JSONConfigModel
from infrastructure.db.models.parque_movil_model import ParqueMovilModel
from infrastructure.db.models.conteo_stock_model import ConteoStockModel

# -----------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Estadísticas Dota",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

pages = {
    "Inicio":[
        st.Page(main, title=PAG_PRINCIPAL),
        st.Page(sissa_page,title=PAG_SISSSA),
        st.Page(dota_licitaciones_page, title=PAG_DOTA_LICITACIONES),
        st.Page(cargar_datos, title=PAG_CARGAR_DATOS)
    ],
    "Estadísticas de consumo":[
        st.Page(consumo_indice, title=PAG_INDICES),
        st.Page(consumo_prevision, title=PAG_PREVISION),
        st.Page(duracion_repuestos, title=PAG_DURACION),
        st.Page(consumo_historial, title=PAG_HISTORIAL),
        st.Page(consumo_obligatorio, title=PAG_CONSUMO_OBLIGATORIO),
    ],
    "Estadísticas de garantías":[
        st.Page(garantias_falla_equipos, title=PAG_FALLA_GARANTIAS),
    ],
    "Estadísticas de gomería":[
        st.Page(gomeria_transferencias_entre_depositos, title=PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)
    ],
    "Datos":[
        st.Page(maximos_minimos, title=PAG_MAXIMOS_MINIMOS),
        st.Page(coches_cabecera, title=PAG_COCHES_CABECERA),
        st.Page(parque_movil, title=PAG_PARQUE_MOVIL)
    ],
}


nav = st.navigation(pages, position="top")

if __name__ == "__main__":
    DBBase.metadata.create_all(db_engine)
    nav.run()
