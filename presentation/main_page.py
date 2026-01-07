import streamlit as st

from config.constants_colors import *
from config.constants_views import LINK_BOX_HEIGHT, LINK_BOX_WIDTH, PAG_PRINCIPAL, PIE_PLOT_BOX_HEIGHT, \
    CONTEO_BOX_HEIGHT, CONTEO_STATS_HEIGHT, CSS_CONTEO
from presentation.streamlit_components import OtherComponents
from viewmodels.conteo_stock.plotter import ConteoStockPlotter
from viewmodels.conteo_stock.vm import ConteoStockVM, calcular_porcentaje


def main():
    components = OtherComponents()
    colors = FALLAS_GARANTIAS_COLORS

    st.title(PAG_PRINCIPAL)
    st.subheader("Conteo Stock 2025")

    pie, stats = st.columns([0.8,1])

    with pie.container(height=CONTEO_BOX_HEIGHT):
        st.plotly_chart(ConteoStockPlotter().create_plot())

    with stats.container(height=CONTEO_BOX_HEIGHT):
        datos = ConteoStockVM().calcular_datos()
        rep_totales = 6000
        rep_contados = datos[5]
        porcentaje = calcular_porcentaje(rep_totales, rep_contados)


        aux, medio, aux2 = st.columns([1,2,1])

        with medio.container(height=CONTEO_STATS_HEIGHT):
            aux5, interno, aux6 = st.columns([1,1,1])

            # interno.metric("CONTEO", rep_contados, f"{porcentaje}%")
            components.custom_metric(interno, "CONTEO", rep_contados, "white", "white", f"{porcentaje}%", "green")
            st.progress(int(porcentaje), str(rep_totales))

        # Datos de conteo
        col1, col2 = st.columns([1,1])
        components.custom_metric(col1, "Precio faltante", num_parser(datos[0]), colors[1], colors[1])
        components.custom_metric(col2, "Precio sobrante", num_parser(datos[1]), colors[2], colors[2])
        col1.divider()
        col2.divider()
        components.custom_metric(col1, "Precio absoluto anterior", num_parser(datos[2]), colors[3], colors[3])
        components.custom_metric(col2, "Precio absoluto actual", num_parser(datos[3]), colors[4], colors[4])

        st.space(3)
        aux, medio, aux2 = st.columns([1,0.60,1])
        components.custom_metric(medio, "Porcentaje diferencia", f"{datos[4]}%", colors[0], colors[0])



def num_parser(val) -> str:
    return (f"{val:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
            )