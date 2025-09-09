import streamlit as st


class StreamlitUtils:
    @staticmethod
    def show_plot(autoplot):
        st.subheader(f"Ultima actualizacion: {autoplot.devolver_fecha()}")

        figs = autoplot.create_plot()
        figs_len = int(len(figs)/2)

        figs1 = figs[figs_len:]
        figs2 = figs[:figs_len]

        col1, col2 = st.columns(2)

        with col1:
            for fig in figs1:
                st.plotly_chart(fig)

        with col2:
            for fig in figs2:
                st.plotly_chart(fig)