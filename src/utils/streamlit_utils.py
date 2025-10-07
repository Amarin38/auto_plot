from typing import Optional

import pandas as pd
import streamlit as st
from io import BytesIO

from src.config.constants import FILE_STRFTIME_DMY
from src.utils.exception_utils import execute_safely


def download_df(df, file_name: str):
    st.download_button(
        label="Descargar 💾",
        data=df,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@execute_safely
def to_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos")
    return output.getvalue()


@execute_safely
def update_layout(fig, title: str, x_title: str, y_title: str, height: Optional[int] = 500, width: Optional[int] = 500):
    fig.update_layout(
        title=title,
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=13)
        ),
        showlegend=True,

        xaxis=dict(
            title=x_title,
            showticklabels=True
        ),

        yaxis=dict(
            title=y_title,
            showticklabels=True
        ),

        height=height,
        width=width,
    )


@execute_safely
def devolver_fecha(df: pd.DataFrame, columna: str) -> str:
    if df.size == 0:
        return ""
    return pd.to_datetime(df[columna].unique()).strftime(FILE_STRFTIME_DMY)[0]