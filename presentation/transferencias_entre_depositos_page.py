import streamlit as st
from babel.numbers import format_decimal

from config.constants import PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS, FULL_PLOT_BOX_TRANSFER_HEIGHT
from utils.streamlit_utils import select_box_cabecera
from viewmodels.diferencia_movimientos_entre_depositos_vm import DiferenciaMovimientosEntreDepositosVM
from viewmodels.plot.transferencias_entre_depositos_plotter import TransferenciasEntreDepositosPlotter

def transferencias_entre_depositos() -> None:
    st.title(PAG_TRANSFERENCIAS_ENTRE_DEPOSITOS)

    transfer, diferencia = st.tabs(["🔛 Transferencias entre depósitos por cabecera", "ℹ️ Diferencias de movimientos"])

    with transfer.container(height=FULL_PLOT_BOX_TRANSFER_HEIGHT):
        aux1, centro, aux2 = st.columns([1,1,1])
        cabecera = select_box_cabecera(centro, "CABECERA_TRANSFERENCIA")

        fig = TransferenciasEntreDepositosPlotter(cabecera).create_plot()

        if fig is not None:
            st.plotly_chart(fig)
        else:
            st.write("Selecciona una cabecera que contenga información.")

    with diferencia:
        df = DiferenciaMovimientosEntreDepositosVM().get_df()
        df["DiferenciaDeCostos"] = df["DiferenciaDeCostos"].fillna(0)

        # TODO: Añadir distintos colores de gradiente para elegir
        styled_df = (df.style
                     .pipe(lambda s: s.background_gradient(subset=["DiferenciaDeCostos"], axis=0,
                                                           gmap=df["DiferenciaDeCostos"], cmap='YlOrRd'))
                     .pipe(lambda s: s.background_gradient(subset=["DiferenciaAnual"], axis=0,
                                                           gmap=df["DiferenciaAnual"], cmap='YlOrRd'))
                     )

        df["DiferenciaDeCostos"] = df["DiferenciaDeCostos"].apply(lambda x: f"$ {format_decimal(round(x), locale='es_AR')}")
        df["CostoTotal2024"] = df["CostoTotal2024"].apply(lambda x: f"$ {format_decimal(round(x), locale='es_AR')}")
        df["CostoTotal2025"] = df["CostoTotal2025"].apply(lambda x: f"$ {format_decimal(round(x), locale='es_AR')}")

        st.write(styled_df)


