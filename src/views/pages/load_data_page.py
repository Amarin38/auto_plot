import os
import sys
import streamlit as st


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.config.constants import PAG_CARGAR_DATOS
from src.config.enums import LoadDataEnum
from src.services.analysis.deviation_trend import DeviationTrend
from src.services.analysis.forecast import create_forecast
from src.services.analysis.garantias import calcular_consumo_garantias, calcular_falla_garantias
from src.services.analysis.index import Index
from src.services.analysis.maxmin import MaxMin
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.utils.common_utils import CommonUtils
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import load_data_bttn, error_dialog, select_box_load_data, select_box_tipo_repuesto, \
    select_box_tipo_indice, select_box_repuesto, select_box_tipo_duracion
from src.services.analysis.duracion_repuestos import DuracionRepuestos


def load_data_page():
    aux1, centro, aux2 = st.columns([3,3,3])
    centro.title(PAG_CARGAR_DATOS)

    with centro:
        uploaded_files = st.file_uploader("Ingresa datos para actualizar", accept_multiple_files="directory")
        select_load = select_box_load_data(st, "LOAD_DATA_LOAD_CENTRO")

        if select_load and len(uploaded_files) > 0:
            match select_load:
                case LoadDataEnum.INDICES_DE_CONSUMO:
                    select_repuesto = select_box_tipo_repuesto(st, "LOAD_DATA_REPUESTO_INDICE")
                    select_tipo_indice = select_box_tipo_indice(st, "LOAD_DATA_TIPO_INDICE_INDICE")

                    if select_repuesto and select_tipo_indice:
                        load_data_bttn(lambda: Index().calculate(load_data(select_load, uploaded_files),
                                                                 select_repuesto.upper(),
                                                                 select_tipo_indice.upper()
                                                                 ))

                case LoadDataEnum.PREVISION_DE_CONSUMO:
                    select_prevision = select_box_tipo_repuesto(st, "LOAD_DATA_TIPO_PREVISION_CONSUMO")

                    if select_prevision:
                        load_data_bttn(lambda: create_forecast(load_data(select_load, uploaded_files),
                                                               select_prevision.upper()
                                                               ))

                case LoadDataEnum.DESVIACION_DE_INDICES:
                    load_data_bttn(lambda: DeviationTrend().calculate(load_data(select_load, uploaded_files)))

                case LoadDataEnum.FALLA_GARANTIAS:
                    load_data_bttn(lambda: calcular_falla_garantias(load_data(select_load, uploaded_files)))

                case LoadDataEnum.CONSUMO_GARANTIAS:
                    load_data_bttn(lambda: calcular_consumo_garantias(load_data(select_load, uploaded_files)))

                case LoadDataEnum.MAXIMOS_Y_MINIMOS:
                    mult_por_min = st.text_input("Multiplicar por: ", 2.5)
                    mult_por_max = st.text_input("Multiplicar por: ", 4)

                    if mult_por_min not in ("0", '', ' ') and mult_por_max not in ("0", '', ' '):
                        load_data_bttn(lambda: MaxMin().calculate(load_data(select_load, uploaded_files),
                                                                  float(mult_por_min),
                                                                  float(mult_por_max)
                                                                  ))
                    else:
                        error_dialog("No se puede multiplicar por 0, por 1 o por None")

                case LoadDataEnum.DURACION_REPUESTOS:
                    select_repuesto = select_box_repuesto(st, "LOAD_DATA_REPUESTO_DURACION")
                    select_tipo = select_box_tipo_duracion(st, "LOAD_DATA_TIPO_DURACION")

                    load_data_bttn(lambda: DuracionRepuestos(load_data(select_load, uploaded_files),
                                                             select_repuesto,
                                                             select_tipo
                                                             ).calcular_duracion()
                                   )


@execute_safely
def load_data(select_load, uploaded_files):
    match select_load:
        case LoadDataEnum.DESVIACION_DE_INDICES | LoadDataEnum.FALLA_GARANTIAS | LoadDataEnum.CONSUMO_GARANTIAS | LoadDataEnum.DURACION_REPUESTOS:
            return CommonUtils().concat_dataframes(uploaded_files)
        case _:
            if uploaded_files and select_load:
                return InventoryDataCleaner().run_all(uploaded_files)
            return None
