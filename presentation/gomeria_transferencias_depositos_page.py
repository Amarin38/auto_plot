import streamlit as st

from config.constants_views import PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, \
    GOMERIA_DIFERENCIA_BOX_HEIGHT, GOMERIA_TRANSFER_BOX_HEIGHT
from presentation.streamlit_components import SelectBoxComponents
from utils.common_utils import CommonUtils
from viewmodels.gomeria.diferencias_mov_plotter import DiferenciaMovimientosEntreDepositosPlotter
from viewmodels.gomeria.transferencias_dep_plotter import TransferenciasEntreDepositosPlotter

@st.cache_data(ttl=200, show_spinner=False)
def _generar_grafico_transferencias(cabecera):
    return TransferenciasEntreDepositosPlotter(cabecera).create_plot()

@st.cache_data(ttl=200, show_spinner=False)
def _generar_grafico_diferencias():
    return DiferenciaMovimientosEntreDepositosPlotter().create_plot()


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
                        fig_transfer = utils.run_in_threads(lambda: _generar_grafico_transferencias(cabecera),
                                                            max_workers=2)

                if fig_transfer is not None:
                    st.plotly_chart(fig_transfer)
                else:
                    st.write("Selecciona una cabecera que contenga información.")

        with diferencia.container(height=GOMERIA_DIFERENCIA_BOX_HEIGHT):
            with st.spinner("Cargando diferencias..."):
                fig_diferencia = utils.run_in_threads(_generar_grafico_diferencias, max_workers=2)

            if fig_diferencia is not None:
                st.plotly_chart(fig_diferencia)
            else:
                st.write("No existen datos de diferencia.")




