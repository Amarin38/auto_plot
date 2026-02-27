import streamlit as st

from config.constants_views import PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, \
    GOMERIA_DIFERENCIA_BOX_HEIGHT, GOMERIA_TRANSFER_BOX_HEIGHT
from presentation.streamlit_components import SelectBoxComponents
from utils.common_utils import CommonUtils
from viewmodels.gomeria.diferencia_mov_dep_vm import DiferenciaMovimientosEntreDepositosVM
from viewmodels.gomeria.diferencias_mov_plotter import DiferenciaMovimientosEntreDepositosPlotter
from viewmodels.gomeria.transferencias_dep_plotter import TransferenciasEntreDepositosPlotter
from viewmodels.gomeria.transferencias_dep_vm import TransferenciasEntreDepositosVM


@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos_transferencias(cabecera):
    return TransferenciasEntreDepositosVM().get_df_by_cabecera(cabecera)


@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos_diferencias():
    return DiferenciaMovimientosEntreDepositosVM().get_df()


def gomeria_transferencias_entre_depositos() -> None:
    select = SelectBoxComponents()
    utils = CommonUtils()
    st.title(PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)
    fig_transfer = None

    with st.container(height=770):
        transfer, diferencia = st.columns([0.5, 1])

        with transfer:
            aux, izq, der = st.columns([0.55, 1,0.6])

            cabecera = select.select_box_cabecera(izq, "CABECERA_TRANSFERENCIA")

            with st.container(height=GOMERIA_TRANSFER_BOX_HEIGHT):
                if cabecera:
                    with st.spinner("Cargando transferencias..."):
                        df_transfer = _cargar_datos_transferencias(cabecera)

                    if not df_transfer.empty:
                        fig_transfer = TransferenciasEntreDepositosPlotter(df_transfer).create_plot()
                        st.plotly_chart(fig_transfer)
                    else:
                        st.write("Selecciona una cabecera que contenga información.")


        with diferencia.container(height=GOMERIA_DIFERENCIA_BOX_HEIGHT):
            with st.spinner("Cargando diferencias..."):
                df_difer = _cargar_datos_diferencias()

            if not df_difer.empty:
                fig_diferencia = DiferenciaMovimientosEntreDepositosPlotter(df_difer).create_plot()
                st.plotly_chart(fig_diferencia)
            else:
                st.write("No existen datos de diferencia.")




