import pandas as pd
import streamlit as st

from config.constants_common import IMG_PATH
from config.constants_views import PAG_CARGAR_DATOS, CARGAR_DATOS_BASIC_HEIGHT, CARGAR_DATOS_MULTI_HEIGHT
from config.enums import LoadDataEnum, TipoCargarEnum, MovimientoEnum

from domain.services.compute_garantias import compute_consumo_garantias, compute_fallas_garantias
from domain.services.compute_consumo_comparacion import compute_comparacion_consumo
from domain.services.compute_consumo_obligatorio import compute_consumo_obligatorio

from domain.services.compute_consumo_historial import compute_historial
from domain.services.compute_consumo_prevision import create_forecast_local
from domain.services.compute_consumo_indices import ConsumoIndice
from domain.services.compute_consumo_duracion_repuestos import DuracionRepuestos
from domain.services.data_cleaner_listado import InventoryDataCleaner

from utils.common_utils import CommonUtils
from utils.exception_utils import execute_safely
from presentation.streamlit_components import ButtonComponents, SelectBoxComponents
from viewmodels.consumo_vm import ConteoStockVM
from viewmodels.datos_vm import ParqueMovilVM, ProveedoresVM, RepuestosCodigosVM, UsuariosCodigosVM
from viewmodels.gomeria_vm import TransferenciasGomeriaVM, DiferenciasGomeriaVM


def cargar_datos():
    buttons = ButtonComponents()
    select = SelectBoxComponents()

    if "height_izq" not in st.session_state:
        st.session_state.height_izq = CARGAR_DATOS_BASIC_HEIGHT

    st.title(PAG_CARGAR_DATOS)

    select_cargar, datos_col = st.columns([1, 4])

    with select_cargar:
        select_load = select.select_box_load_data(st, "LOAD_DATA_LOAD_CENTRO")
        if select_load:
            with st.expander("Ejemplo de excel a insertar"):
                st.image(f"{IMG_PATH}{str(select_load).lower()}.png", caption="Como se debe ver la tabla a insertar")

    with datos_col:
        tipo, cargar = st.columns([2, 2])
        datos = None

        with tipo.container(height=st.session_state.height_izq):
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

        with cargar:
            if select_load and uploaded_files is not None:
                match select_load:
                        case LoadDataEnum.INDICES_DE_CONSUMO:
                            select_repuesto = select.select_box_tipo_repuesto(st, "LOAD_DATA_REPUESTO_INDICE")
                            select_tipo_indice = select.select_box_tipo_indice(st, "LOAD_DATA_TIPO_INDICE_INDICE")

                            if select_repuesto and select_tipo_indice:
                                datos = lambda: ConsumoIndice().calculate(load_data(select_load, uploaded_files),
                                                                  select_repuesto.upper(),
                                                                  select_tipo_indice.upper())

                        case LoadDataEnum.PREVISION_DE_CONSUMO:
                            select_prevision = select.select_box_tipo_repuesto(st, "LOAD_DATA_TIPO_PREVISION_CONSUMO")

                            if select_prevision:
                                datos = lambda: create_forecast_local(load_data(select_load, uploaded_files),
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

                        case LoadDataEnum.DURACION_REPUESTOS:
                            select_tipo = select.select_box_tipo_duracion(st, "LOAD_DATA_TIPO_DURACION")

                            if select_tipo:
                                datos = lambda: DuracionRepuestos(load_data(select_load, uploaded_files),
                                                                  select_tipo).calcular_duracion()

                        case LoadDataEnum.TRANSFERENCIAS_ENTRE_DEPOSITOS:
                            datos = lambda: TransferenciasGomeriaVM().save(load_data(select_load, uploaded_files))

                        case LoadDataEnum.DIFERENCIA_MOVIMIENTOS_ENTRE_DEPOSITOS:
                            datos = lambda: DiferenciasGomeriaVM().save(load_data(select_load, uploaded_files))

                        case LoadDataEnum.PARQUE_MOVIL:
                            datos = lambda: ParqueMovilVM().save(load_data(select_load, uploaded_files))

                        case LoadDataEnum.CONTEO_STOCK:
                            datos = lambda: ConteoStockVM().save(load_data(select_load, uploaded_files))

                        case LoadDataEnum.COMPARACION_CONSUMO:
                            select_repuesto = select.select_box_tipo_rep_comparacion(st, "LOAD_DATA_TIPO_COMPARACION")

                            if select_repuesto:
                                datos = lambda: compute_comparacion_consumo(load_data(select_load, uploaded_files),
                                                                            select_repuesto)

                        case LoadDataEnum.USUARIOS_CODIGOS:
                            datos = lambda: UsuariosCodigosVM().save(load_data(select_load, uploaded_files))

                        case LoadDataEnum.REPUESTOS_CODIGOS:
                            vm = RepuestosCodigosVM()
                            df = vm.formatear_df(load_data(select_load, uploaded_files))
                            datos = lambda: vm.save(df)

                        case LoadDataEnum.PROVEEDORES:
                            datos = lambda: ProveedoresVM().save(load_data(select_load, uploaded_files))

                        case LoadDataEnum.GOMERIA_MOVIMIENTOS:
                            ...
    with tipo:
        if datos is not None and uploaded_files not in ([None], []):
            buttons.load_data_bttn(datos)


@execute_safely
def load_data(select_load: LoadDataEnum, uploaded_files):
    match select_load:
        case   LoadDataEnum.PARQUE_MOVIL                    | LoadDataEnum.FALLA_GARANTIAS \
             | LoadDataEnum.CONSUMO_GARANTIAS               | LoadDataEnum.DURACION_REPUESTOS \
             | LoadDataEnum.TRANSFERENCIAS_ENTRE_DEPOSITOS  | LoadDataEnum.DIFERENCIA_MOVIMIENTOS_ENTRE_DEPOSITOS \
             | LoadDataEnum.CONSUMO_OBLIGATORIO             | LoadDataEnum.CONTEO_STOCK \
             | LoadDataEnum.USUARIOS_CODIGOS                | LoadDataEnum.REPUESTOS_CODIGOS \
             | LoadDataEnum.PROVEEDORES:
            return CommonUtils().concat_dataframes(uploaded_files)
        case _:
            if uploaded_files and select_load:
                if LoadDataEnum.COMPARACION_CONSUMO:
                    return InventoryDataCleaner().run_all(uploaded_files, MovimientoEnum.TRANSFERENCIAS)
                return InventoryDataCleaner().run_all(uploaded_files, MovimientoEnum.SALIDAS)
            return pd.DataFrame()
