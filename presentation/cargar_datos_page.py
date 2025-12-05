import streamlit as st

from config.constants_views import PAG_CARGAR_DATOS
from config.enums import LoadDataEnum, TipoCargarEnum
from viewmodels.common.parque_movil_vm import ParqueMovilVM
from viewmodels.gomeria.diferencia_mov_dep_vm import DiferenciaMovimientosEntreDepositosVM
from viewmodels.processing.compute.compute_consumo_obligatorio import compute_consumo_obligatorio

from viewmodels.processing.compute.compute_desviacion_indices import DeviationTrend
from viewmodels.processing.compute.compute_historial_consumo import compute_historial
from viewmodels.processing.compute.compute_prevision import create_forecast
from viewmodels.processing.compute.compute_garantias import compute_consumo_garantias, compute_fallas_garantias
from viewmodels.processing.compute.compute_indices_consumo import Index
from viewmodels.processing.compute.compute_maximos_minimos import MaxMin
from viewmodels.processing.compute.compute_duracion_repuestos import DuracionRepuestos

from viewmodels.processing.data_cleaning.listado_data_cleaner import InventoryDataCleaner

from utils.common_utils import CommonUtils
from utils.exception_utils import execute_safely
from viewmodels.gomeria.transferencias_dep_vm import TransferenciasEntreDepositosVM
from presentation.streamlit_components import ButtonComponents, SelectBoxComponents, DialogComponents


def cargar_datos():
    buttons = ButtonComponents()
    select = SelectBoxComponents()
    dialog = DialogComponents()

    aux1, centro, aux2 = st.columns([3,3,3])
    centro.title(PAG_CARGAR_DATOS)

    with centro:
        tipo_cargar = st.radio("Selecciona el tipo de ingreso", [TipoCargarEnum.UNICO, TipoCargarEnum.MULTIPLE],
                               captions=["Seleccion de archivos simple", "Seleccion de archivos por carpeta"])

        match tipo_cargar:
            case TipoCargarEnum.UNICO:
                uploaded_files = st.file_uploader("Ingresa datos para actualizar")
                if uploaded_files:
                    uploaded_files = [uploaded_files]
            case TipoCargarEnum.MULTIPLE:
                uploaded_files = st.file_uploader("Ingresa datos para actualizar", accept_multiple_files="directory")
            case _:
                uploaded_files = None


        select_load = select.select_box_load_data(st, "LOAD_DATA_LOAD_CENTRO")

        if select_load and uploaded_files is not None:

            match select_load:
                case LoadDataEnum.INDICES_DE_CONSUMO:
                    st.image("resources/indice_consumo.png", caption="Como se debe ver la tabla a insertar")
                    select_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_REPUESTO_INDICE")
                    select_tipo_indice = select.select_box_tipo_indice(st, "LOAD_DATA_TIPO_INDICE_INDICE")

                    if select_repuesto and select_tipo_indice:
                        buttons.load_data_bttn(lambda: Index().calculate(load_data(select_load, uploaded_files),
                                                                 select_repuesto.upper(),
                                                                 select_tipo_indice.upper()))

                case LoadDataEnum.PREVISION_DE_CONSUMO:
                    st.image("resources/prevision_consumo.png", caption="Como se debe ver la tabla a insertar")
                    select_prevision = select.select_box_tipo_repuesto(st, "LOAD_DATA_TIPO_PREVISION_CONSUMO")

                    if select_prevision:
                        buttons.load_data_bttn(lambda: create_forecast(load_data(select_load, uploaded_files),
                                                               select_prevision.upper()))

                case LoadDataEnum.HISTORIAL_CONSUMO:
                    st.image("resources/historial_consumo.png", caption="Como se debe ver la tabla a insertar")
                    select_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_REPUESTO_HISTORIAL")

                    if select_repuesto:
                        buttons.load_data_bttn(lambda: compute_historial(load_data(select_load, uploaded_files),
                                                                 select_repuesto))

                case LoadDataEnum.CONSUMO_OBLIGATORIO:
                    st.image("resources/consumo_obligatorio.png", caption="Como se debe ver la tabla a insertar")
                    select_repuesto = select.select_box_consumo_obligatorio(st, "LOAD_DATA_REPUESTO_CONSUMO_OBLIGATORIO")

                    if select_repuesto:
                        buttons.load_data_bttn(lambda: compute_consumo_obligatorio(load_data(select_load, uploaded_files),
                                                                           select_repuesto))

                case LoadDataEnum.FALLA_GARANTIAS:
                    st.image("resources/datos_garantias.png", caption="Como se debe ver la tabla a insertar")
                    select_tipo_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_TIPO_REPUESTO_FALLAS")

                    buttons.load_data_bttn(lambda: compute_fallas_garantias(load_data(select_load, uploaded_files),
                                                                    select_tipo_repuesto))

                case LoadDataEnum.CONSUMO_GARANTIAS:
                    st.image("resources/datos_garantias.png", caption="Como se debe ver la tabla a insertar")
                    select_tipo_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_TIPO_REPUESTO_CONSUMO")

                    buttons.load_data_bttn(lambda: compute_consumo_garantias(load_data(select_load, uploaded_files),
                                                                     select_tipo_repuesto))

                case LoadDataEnum.MAXIMOS_Y_MINIMOS:
                    st.image("resources/maxmins.png", caption="Como se debe ver la tabla a insertar")
                    mult_por_min = st.text_input("Multiplicar al mínimo por: ", 2)
                    mult_por_max = st.text_input("Multiplicar al máximo por: ", 3)

                    if mult_por_min not in ("0", '', ' ') and mult_por_max not in ("0", '', ' '):
                        buttons.load_data_bttn(lambda: MaxMin().calculate(load_data(select_load, uploaded_files),
                                                                  float(mult_por_min),
                                                                  float(mult_por_max)))
                    else:
                        dialog.error_dialog("No se puede multiplicar por 0, por 1 o por None")

                case LoadDataEnum.DURACION_REPUESTOS:
                    st.image("resources/duracion.png", caption="Como se debe ver la tabla a insertar")
                    select_repuesto = select.select_box_repuesto(st, "LOAD_DATA_REPUESTO_DURACION")
                    select_tipo = select.select_box_tipo_duracion(st, "LOAD_DATA_TIPO_DURACION")

                    buttons.load_data_bttn(lambda: DuracionRepuestos(load_data(select_load, uploaded_files),
                                                             select_repuesto,
                                                             select_tipo
                                                             ).calcular_duracion())

                case LoadDataEnum.TRANSFERENCIAS_ENTRE_DEPOSITOS:
                    st.image("resources/transfer_entre_depo.png", caption="Como se debe ver la tabla a insertar")
                    buttons.load_data_bttn(lambda: TransferenciasEntreDepositosVM().save_df(
                        load_data(select_load, uploaded_files)))

                case LoadDataEnum.DIFERENCIA_MOVIMIENTOS_ENTRE_DEPOSITOS:
                    st.image("resources/difer_entre_depo.png", caption="Como se debe ver la tabla a insertar")
                    buttons.load_data_bttn(lambda: DiferenciaMovimientosEntreDepositosVM().save_df(
                        load_data(select_load, uploaded_files)))

                case LoadDataEnum.PARQUE_MOVIL:
                    st.image("resources/parque.png", caption="Como se debe ver la tabla a insertar")
                    print(uploaded_files)
                    buttons.load_data_bttn(lambda: ParqueMovilVM().save_df(load_data(select_load, uploaded_files)))

@execute_safely
def load_data(select_load: LoadDataEnum , uploaded_files):
    match select_load:
        case   LoadDataEnum.PARQUE_MOVIL | LoadDataEnum.FALLA_GARANTIAS \
             | LoadDataEnum.CONSUMO_GARANTIAS | LoadDataEnum.DURACION_REPUESTOS \
             | LoadDataEnum.TRANSFERENCIAS_ENTRE_DEPOSITOS | LoadDataEnum.DIFERENCIA_MOVIMIENTOS_ENTRE_DEPOSITOS \
             | LoadDataEnum.CONSUMO_OBLIGATORIO:
            return CommonUtils().concat_dataframes(uploaded_files)
        case _:
            if uploaded_files and select_load:
                return InventoryDataCleaner().run_all(uploaded_files)
            return None
