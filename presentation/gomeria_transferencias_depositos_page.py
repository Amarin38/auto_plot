import streamlit as st
from babel.numbers import format_decimal

from config.constants_views import PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, FULL_PLOT_BOX_TRANSFER_HEIGHT, SELECT_BOX_HEIGHT, \
    PLACEHOLDER, GOMERIA_BOX_HEIGHT
from config.enums import ColoresMatplotlibEnum
from presentation.streamlit_components import SelectBoxComponents, OtherComponents
from viewmodels.gomeria.diferencia_mov_dep_vm import DiferenciaMovimientosEntreDepositosVM
from viewmodels.gomeria.diferencias_mov_plotter import DiferenciaMovimientosEntreDepositosPlotter
from viewmodels.gomeria.transferencias_dep_plotter import TransferenciasEntreDepositosPlotter


def gomeria_transferencias_entre_depositos() -> None:
    select = SelectBoxComponents()
    st.title(PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)

    transfer, diferencia = st.columns([0.5,1])

    with transfer:
        aux, izq, der = st.columns([0.6, 1,0.6])

        cabecera = select.select_box_cabecera(izq, "CABECERA_TRANSFERENCIA")
        fig_transfer = TransferenciasEntreDepositosPlotter(cabecera).create_plot()

        with st.container(height=600):
            if fig_transfer is not None:
                st.plotly_chart(fig_transfer)
            else:
                st.write("Selecciona una cabecera que contenga información.")

    with diferencia.container(height=GOMERIA_BOX_HEIGHT):
        fig_diferencia = DiferenciaMovimientosEntreDepositosPlotter().create_plot()

        if fig_diferencia is not None:
            st.plotly_chart(fig_diferencia)
        else:
            st.write("No existen datos de diferencia.")





