import sys, os

import streamlit as st



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.db_data import CommonBase, ServicesBase
from src.db_data import common_engine, services_engine

from src.views.pages.forecast_page import forecast_page
from src.views.pages.deviation_page import deviation_page
from src.views.pages.maxmin_page import maxmin_page
from src.views.pages.main_page import main_page
from src.views.pages.index_page import index_page
from src.views.pages.load_data_page import load_data_page

from src.views.pages.falla_equipos_garantia_page import falla_equipos_garantias_page

from src.config.constants import PAG_PRINCIPAL, PAG_CARGAR_DATOS, PAG_INDICES, PAG_PREVISION, PAG_DESVIACIONES, \
    PAG_FALLA_GARANTIAS, PAG_MAXMIN

# Services DB -----------------------------------------------------------------------------------
from src.db_data.models.services_model.deviation_model import  DeviationModel
from src.db_data.models.services_model.maxmin_model import MaxminModel
from src.db_data.models.services_model.consumo_garantias_model import ConsumoGarantiasModel
from src.db_data.models.services_model.forecast_model import ForecastModel
from src.db_data.models.services_model.forecast_data_model import ForecastDataModel
from src.db_data.models.services_model.falla_garantias_model import FallaGarantiasModel
from src.db_data.models.services_model.index_repuesto_model import IndexRepuestoModel

# Common DB -----------------------------------------------------------------------------------
from src.db_data.models.config_model.chasis_model import ChasisModel
from src.db_data.models.config_model.cilindros_model import CilindrosModel
from src.db_data.models.config_model.coches_cabecera_model import CochesCabeceraModel
from src.db_data.models.config_model.coches_cabecera_new_model import CochesCabeceraNewModel
from src.db_data.models.config_model.datos_garantias_model import DatosGarantiasModel
from src.db_data.models.config_model.internos_asignados_model import InternosAsignadosModel
from src.db_data.models.config_model.internos_cabecera_model import InternosCabeceraModel
from src.db_data.models.config_model.json_config_model import JSONConfigModel
from src.db_data.models.config_model.motores_cabecera_model import MotoresCabeceraModel
from src.db_data.models.config_model.motores_model import MotoresModel
from src.db_data.models.config_model.normativa_model import NormativaModel

# -----------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Estadisticas Dota",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

# LoadDataSideBar().select_data()

pages = {
    "Inicio":[
        st.Page(main_page, title=PAG_PRINCIPAL),
        st.Page(load_data_page, title=PAG_CARGAR_DATOS)
    ],
    "Estadísticas":[
        st.Page(index_page, title=PAG_INDICES),
        st.Page(forecast_page, title=PAG_PREVISION),
        st.Page(deviation_page, title=PAG_DESVIACIONES),
        st.Page(falla_equipos_garantias_page, title=PAG_FALLA_GARANTIAS),
        st.Page(maxmin_page, title=PAG_MAXMIN)
    ]
}

nav = st.navigation(pages, position="top")

if __name__ == "__main__":
    CommonBase.metadata.create_all(common_engine)
    ServicesBase.metadata.create_all(services_engine)

    nav.run()