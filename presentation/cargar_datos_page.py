import pandas as pd
import streamlit as st

from config.constants_common import IMG_PATH
from config.constants_views import PAG_CARGAR_DATOS, CARGAR_DATOS_BASIC_HEIGHT, CARGAR_DATOS_MULTI_HEIGHT, INPUT_HEIGHT
from config.enums import LoadDataEnum, TipoCargarEnum, MovimientoEnum
from domain.services.compute_comparacion_consumo import compute_comparacion_consumo
from viewmodels.common.parque_movil_vm import ParqueMovilVM
from viewmodels.conteo_stock.vm import ConteoStockVM
from viewmodels.gomeria.diferencia_mov_dep_vm import DiferenciaMovimientosEntreDepositosVM
from domain.services.compute_consumo_obligatorio import compute_consumo_obligatorio

from domain.services.compute_historial_consumo import compute_historial
from domain.services.compute_prevision import create_forecast
from domain.services.compute_garantias import compute_consumo_garantias, compute_fallas_garantias
from domain.services.compute_indices_consumo import Index
from domain.services.compute_maximos_minimos import MaxMin
from domain.services.compute_duracion_repuestos import DuracionRepuestos

from domain.services.data_cleaner_listado import InventoryDataCleaner

from utils.common_utils import CommonUtils
from utils.exception_utils import execute_safely
from viewmodels.gomeria.transferencias_dep_vm import TransferenciasEntreDepositosVM
from presentation.streamlit_components import ButtonComponents, SelectBoxComponents, DialogComponents



def cargar_datos():
    buttons = ButtonComponents()
    select = SelectBoxComponents()
    dialog = DialogComponents()

    if "height_izq" not in st.session_state:
        st.session_state.height_izq = CARGAR_DATOS_BASIC_HEIGHT

    st.title(PAG_CARGAR_DATOS)

    aux1, aux2 = st.columns([1, 4])

    with aux1:
        select_load = select.select_box_load_data(st, "LOAD_DATA_LOAD_CENTRO")
        if select_load:
            with st.expander("Ejemplo de excel a insertar"):
                st.image(f"{IMG_PATH}{str(select_load).lower()}.png", caption="Como se debe ver la tabla a insertar")

    with aux2:
        izq, der = st.columns([2, 2])
        datos = None

        with izq.container(height=st.session_state.height_izq):
            tipo_cargar = st.radio("Selecciona el tipo de ingreso:", [TipoCargarEnum.UNICO, TipoCargarEnum.MULTIPLE],
                                   captions=["Seleccion de archivos simple", "Seleccion de archivos por carpeta"])

            match tipo_cargar:
                case TipoCargarEnum.UNICO:
                    uploaded_files = [st.file_uploader("Ingresa datos para actualizar")]

                    if st.session_state.height_izq != CARGAR_DATOS_BASIC_HEIGHT:
                        st.session_state.height_izq = CARGAR_DATOS_BASIC_HEIGHT
                        st.rerun()

                case TipoCargarEnum.MULTIPLE:
                    uploaded_files = st.file_uploader("Ingresa datos para actualizar", accept_multiple_files="directory")

                    if st.session_state.height_izq != CARGAR_DATOS_MULTI_HEIGHT:
                        st.session_state.height_izq = CARGAR_DATOS_MULTI_HEIGHT
                        st.rerun()

                case _:
                    uploaded_files = None


        with der:
            if select_load and uploaded_files is not None:
                match select_load:
                        case LoadDataEnum.INDICES_DE_CONSUMO:
                            select_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_REPUESTO_INDICE")
                            select_tipo_indice = select.select_box_tipo_indice(st, "LOAD_DATA_TIPO_INDICE_INDICE")

                            if select_repuesto and select_tipo_indice:
                                datos = lambda: Index().calculate(load_data(select_load, uploaded_files),
                                                                  select_repuesto.upper(),
                                                                  select_tipo_indice.upper())

                        case LoadDataEnum.PREVISION_DE_CONSUMO:
                            select_prevision = select.select_box_tipo_repuesto(st, "LOAD_DATA_TIPO_PREVISION_CONSUMO")

                            if select_prevision:
                                datos = lambda: create_forecast(load_data(select_load, uploaded_files),
                                                                select_prevision.upper())

                        case LoadDataEnum.HISTORIAL_CONSUMO:
                            select_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_REPUESTO_HISTORIAL")

                            if select_repuesto:
                                datos = lambda: compute_historial(load_data(select_load, uploaded_files),
                                                                  select_repuesto)

                        case LoadDataEnum.CONSUMO_OBLIGATORIO:
                            select_repuesto = select.select_box_consumo_obligatorio(st, "LOAD_DATA_REPUESTO_CONSUMO_OBLIGATORIO")

                            if select_repuesto:
                                datos = lambda: compute_consumo_obligatorio(load_data(select_load, uploaded_files),
                                                                            select_repuesto)

                        case LoadDataEnum.FALLA_GARANTIAS:
                            select_tipo_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_TIPO_REPUESTO_FALLAS")

                            if select_tipo_repuesto:
                                datos = lambda: compute_fallas_garantias(load_data(select_load, uploaded_files),
                                                                         select_tipo_repuesto)

                        case LoadDataEnum.CONSUMO_GARANTIAS:
                            select_tipo_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_TIPO_REPUESTO_CONSUMO")

                            if select_tipo_repuesto:
                                datos = lambda: compute_consumo_garantias(load_data(select_load, uploaded_files),
                                                                          select_tipo_repuesto)

                        case LoadDataEnum.MAXIMOS_Y_MINIMOS:
                            with st.container(height=INPUT_HEIGHT):
                                mult_por_min = st.text_input("Multiplicar al mínimo por: ", 2)

                            with st.container(height=INPUT_HEIGHT):
                                mult_por_max = st.text_input("Multiplicar al máximo por: ", 3)

                            if mult_por_min not in ("0", '', ' ') and mult_por_max not in ("0", '', ' '):
                                datos = lambda: MaxMin().calculate(load_data(select_load, uploaded_files),
                                                                   float(mult_por_min),
                                                                   float(mult_por_max))
                            else:
                                dialog.error_dialog("No se puede multiplicar por 0, por 1 o por None")


                        case LoadDataEnum.DURACION_REPUESTOS:
                            select_repuesto = select.select_box_repuesto(st, "LOAD_DATA_REPUESTO_DURACION")
                            select_tipo = select.select_box_tipo_duracion(st, "LOAD_DATA_TIPO_DURACION")

                            if select_repuesto and select_tipo:
                                datos = lambda: DuracionRepuestos(load_data(select_load, uploaded_files),
                                                                  select_repuesto,
                                                                  select_tipo
                                                                  ).calcular_duracion()


                        case LoadDataEnum.TRANSFERENCIAS_ENTRE_DEPOSITOS:
                            datos = lambda: TransferenciasEntreDepositosVM().save_df(
                                            load_data(select_load, uploaded_files))


                        case LoadDataEnum.DIFERENCIA_MOVIMIENTOS_ENTRE_DEPOSITOS:
                            datos = lambda: DiferenciaMovimientosEntreDepositosVM().save_df(
                                            load_data(select_load, uploaded_files))


                        case LoadDataEnum.PARQUE_MOVIL:
                            datos = lambda: ParqueMovilVM().save_df(load_data(select_load, uploaded_files))


                        case LoadDataEnum.CONTEO_STOCK:
                            datos = lambda: ConteoStockVM().save_df(load_data(select_load, uploaded_files))


                        case LoadDataEnum.COMPARACION_CONSUMO:
                            select_repuesto = select.select_box_tipo_rep_comparacion(st, "LOAD_DATA_TIPO_COMPARACION")

                            if select_repuesto:
                                datos = lambda: compute_comparacion_consumo(load_data(select_load, uploaded_files),
                                                                            select_repuesto)

    with aux1:
        if datos is not None and uploaded_files not in ([None], []):
            buttons.load_data_bttn(datos)


@execute_safely
def load_data(self, select_load: LoadDataEnum, uploaded_files):
    match select_load:
        case   LoadDataEnum.PARQUE_MOVIL                    | LoadDataEnum.FALLA_GARANTIAS \
             | LoadDataEnum.CONSUMO_GARANTIAS               | LoadDataEnum.DURACION_REPUESTOS \
             | LoadDataEnum.TRANSFERENCIAS_ENTRE_DEPOSITOS  | LoadDataEnum.DIFERENCIA_MOVIMIENTOS_ENTRE_DEPOSITOS \
             | LoadDataEnum.CONSUMO_OBLIGATORIO             | LoadDataEnum.CONTEO_STOCK:
            return CommonUtils().concat_dataframes(uploaded_files)
        case _:
            if uploaded_files and select_load:
                if LoadDataEnum.COMPARACION_CONSUMO:
                    return InventoryDataCleaner().run_all(uploaded_files, MovimientoEnum.TRANSFERENCIAS)
                return InventoryDataCleaner().run_all(uploaded_files, MovimientoEnum.SALIDAS)
            return pd.DataFrame()
