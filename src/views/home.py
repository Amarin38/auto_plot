import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.db import CommonBase, ServicesBase
from src.db import common_engine, services_engine

from src.db.models.coches_cabecera_model import CochesCabeceraModel
from src.db.models.internos_cabecera_model import InternosCabeceraModel
from src.db.models.motores_cabecera_model import MotoresCabeceraModel
from src.db.models.forecast_data_model import ForecastDataModel
from src.db.models.forecast_trend_model import ForecastTrendModel
from src.db.models.index_repuesto_model import IndexRepuestoModel
from src.db.models.internos_asignados_model import InternosAsignadosModel
from src.db.models.deviation_model import DeviationModel
from src.db.models.maxmin_model import MaxminModel

from src.views.index_view import IndexPage
from src.views.forecast_view import ForecastPage
from src.views.deviation_view import DeviationPage
from src.views.maxmin_view import MaxminPage


def main():
    st.title("Estadisticas repuestos")
    st.set_page_config(
        page_title="Estadisticas",
        page_icon="📊",
        layout="wide",
        )
    
    main, indices, prevision, desviacion, maxmins = st.tabs(["Página principal", "Índices de consumo", "Previsión de consumo", "Desviacion de indices", "Máximos y Mínimos"])


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