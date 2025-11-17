import streamlit as st
from babel.numbers import format_decimal

from config.constants import PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, FULL_PLOT_BOX_TRANSFER_HEIGHT, SELECT_BOX_HEIGHT, \
    PLACEHOLDER
from config.enums import ColoresMatplotlibEnum
from utils.streamlit_utils import select_box_cabecera
from viewmodels.gomeria.diferencia_mov_dep_vm import DiferenciaMovimientosEntreDepositosVM
from viewmodels.gomeria.transferencias_dep_plotter import TransferenciasEntreDepositosPlotter

def transferencias_entre_depositos() -> None:
    st.title(PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)

    transfer, diferencia = st.tabs(["🔛 Transferencias entre depósitos por cabecera", "ℹ️ Diferencias de movimientos"])


    with transfer:
        aux1, centro, aux2 = st.columns([0.5,1,1])
        cabecera = select_box_cabecera(aux1, "CABECERA_TRANSFERENCIA")

    with transfer.container(height=FULL_PLOT_BOX_TRANSFER_HEIGHT):
        fig = TransferenciasEntreDepositosPlotter(cabecera).create_plot()

        if fig is not None:
            st.plotly_chart(fig)
        else:
            st.write("Selecciona una cabecera que contenga información.")

    with diferencia:
        df = DiferenciaMovimientosEntreDepositosVM().get_df()
        aux1, centro, aux2 = st.columns([0.5,1,1])

        with aux1.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
            color = st.selectbox("Selecciona la el color del cuadro:", ColoresMatplotlibEnum , index=None,
                                 placeholder=PLACEHOLDER)

        if color is None:
            color = ColoresMatplotlibEnum.YlOrRd

        styled_df = (df.style
                     .pipe(lambda s: s.background_gradient(subset=["DiferenciaDeCostos"], axis=0,
                                                           gmap=df["DiferenciaDeCostos"], cmap=color))
                     .pipe(lambda s: s.background_gradient(subset=["DiferenciaAnual"], axis=0,
                                                           gmap=df["DiferenciaAnual"], cmap=color))
                     )

        df["DiferenciaDeCostos"] = df["DiferenciaDeCostos"].apply(lambda x: f"$ {format_decimal(round(x), locale='es_AR')}")
        df["CostoTotal2024"] = df["CostoTotal2024"].apply(lambda x: f"$ {format_decimal(round(x), locale='es_AR')}")
        df["CostoTotal2025"] = df["CostoTotal2025"].apply(lambda x: f"$ {format_decimal(round(x), locale='es_AR')}")

        st.write(styled_df)


