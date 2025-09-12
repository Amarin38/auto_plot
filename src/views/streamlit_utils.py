import pandas as pd
import streamlit as st
from io import BytesIO

from src.utils.exception_utils import execute_safely


class StreamlitUtils:
    @staticmethod
    def show_plot(autoplot, rep: str):
        st.subheader(autoplot.devolver_titulo(rep))

        figs = autoplot.create_plot()
        figs_len = int(len(figs)/2)

        figs1 = figs[figs_len:]
        figs2 = figs[:figs_len]

        col1, col2 = st.columns(2)
        
        with col1.container(height=475):
            for fig in figs1:
                st.plotly_chart(fig)

        with col2.container(height=475):
            for fig in figs2:
                st.plotly_chart(fig)


    @staticmethod
    def download_df(df, file_name: str):
        st.download_button(
            label="Descargar 💾",
            data=df,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    
    @staticmethod
    @execute_safely
    def to_excel(df: pd.DataFrame) -> bytes:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Datos")
        return output.getvalue()
    