import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.db_data import CommonBase, ServicesBase
from src.db_data import common_engine, services_engine

from src.db_data.models.services_model.forecast_data_model import ForecastDataModel
from src.db_data.models.services_model.forecast_trend_model import ForecastTrendModel
from src.db_data.models.services_model.index_repuesto_model import IndexRepuestoModel
from src.db_data.models.services_model.deviation_model import DeviationModel
from src.db_data.models.services_model.maxmin_model import MaxminModel

from src.db_data.models.config_model.coches_cabecera_model import CochesCabeceraModel
from src.db_data.models.config_model.internos_cabecera_model import InternosCabeceraModel
from src.db_data.models.config_model.motores_cabecera_model import MotoresCabeceraModel
from src.db_data.models.config_model.internos_asignados_model import InternosAsignadosModel
from src.db_data.models.config_model.cilindros_model import CilindrosModel
from src.db_data.models.config_model.normativa_model import NormativaModel
from src.db_data.models.config_model.motores_model import MotoresModel
from src.db_data.models.config_model.chasis_model import ChasisModel

from src.views.index_view import IndexPage
from src.views.forecast_view import ForecastPage
from src.views.deviation_view import DeviationPage
from src.views.maxmin_view import MaxminPage
from src.views.sidebar_view import LoadDataSideBar

def main():
    st.title("Estadisticas repuestos")
    st.set_page_config(
        page_title="Estadisticas",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
        )
    
    main, indices, prevision, desviacion, maxmins = st.tabs(["Página principal", "Índices de consumo", "Previsión de consumo", "Desviacion de indices", "Máximos y Mínimos"])

    LoadDataSideBar().select_data()

    with main:
        st.text("Pagina principal")
    with indices:
        IndexPage().indice_options()
    with prevision:
        ForecastPage().prevision_options()
    with desviacion:
        DeviationPage().show_deviation()
    with maxmins:
        MaxminPage().show_table()


if __name__ == "__main__":
    CommonBase.metadata.create_all(common_engine)
    ServicesBase.metadata.create_all(services_engine)

    main()