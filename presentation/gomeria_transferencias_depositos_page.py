import streamlit as st

from config.constants_views import PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, \
    GOMERIA_DIFERENCIA_BOX_HEIGHT, GOMERIA_TRANSFER_BOX_HEIGHT
from presentation.streamlit_components import SelectBoxComponents
from plotters.gomeria_transferencias_plotter import TransferenciasEntreDepositosPlotter
from viewmodels.gomeria_vm import TransferenciasGomeriaVM, DiferenciasGomeriaVM


@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos_transferencias(cabecera):
    return TransferenciasGomeriaVM().get_df_by_cabecera(cabecera)

@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos_diferencias():
    return DiferenciasGomeriaVM().get_df()


def gomeria_transferencias_entre_depositos() -> None:
    select = SelectBoxComponents()
    plotter = TransferenciasEntreDepositosPlotter()
    st.title(PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)

    with st.container(height=770):
        transfer, diferencia = st.columns([0.5, 1])

        with transfer:
            _, izq, der = st.columns([0.55, 1,0.6])

            cabecera = select.select_box_cabecera(izq, "CABECERA_TRANSFERENCIA")

            with st.container(height=GOMERIA_TRANSFER_BOX_HEIGHT):
                if cabecera:
                    with st.spinner("Cargando transferencias..."):
                        df_transfer = _cargar_datos_transferencias(cabecera)

                    if len(df_transfer):
                        st.plotly_chart(
                            plotter.create_transferencias_plot(df_transfer)
                        )
                    else:
                        st.write("Selecciona una cabecera que contenga información.")

        with diferencia.container(height=GOMERIA_DIFERENCIA_BOX_HEIGHT):
            with st.spinner("Cargando diferencias..."):
                df_difer = _cargar_datos_diferencias()

            if len(df_difer):
                st.plotly_chart(
                    plotter.create_diferencia_plot(df_difer)
                )
            else:
                st.write("No existen datos de diferencia.")




