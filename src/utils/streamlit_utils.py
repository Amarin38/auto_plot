from typing import Optional

import pandas as pd
import streamlit as st
from io import BytesIO

from src.config.constants import FILE_STRFTIME_DMY, COLORS, CENTERED_TITLE_HEIGHT, CENTERED_TITLE_WIDTH, PLACEHOLDER, \
    SELECT_BOX_HEIGHT
from src.utils.exception_utils import execute_safely


@execute_safely
def load_data_bttn(func):
    st.button(
        label="Cargar datos",
        type="primary",
        use_container_width=True,
        on_click=func
    )

@execute_safely
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
    with pd.ExcelWriter(output, engine="openpyxl") as writer: # type: ignore
        df.to_excel(writer, index=False, sheet_name="Datos")
    return output.getvalue()


@execute_safely
def update_layout(fig, title: str, x_title: str, y_title: str, height: Optional[int] = 500, width: Optional[int] = 500):
    fig.update_layout(
        title=title,
        legend=dict(
            orientation='v',
            y=1.02,
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
def top_right_legend(fig):
    fig.update_layout(
        legend=dict(
            orientation='v',
            yanchor='top',
            y=1.15,
            xanchor='right',
            x=1,
            font=dict(size=13),
            bgcolor=COLORS[-1],
            bordercolor=COLORS[5],
        ),
    )


@execute_safely
def range_slider(fig):
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1 Mes",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6 Meses",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="1 Año",
                         step="year",
                         stepmode="backward"),
                    dict(count=2,
                         label="2 Años",
                         step="year",
                         stepmode="backward"),
                    dict(count=3,
                         label="3 Años",
                         step="year",
                         stepmode="backward"),
                    dict(label="Todo",
                         step="all")
                ]),
            ),
            rangeslider=dict(
                visible=True,
                bgcolor="white",
                bordercolor="#0e1117",
                thickness=0.02,
                borderwidth=2,
            ),
            type="date"
        )
    )


@execute_safely
def devolver_fecha(df: pd.DataFrame, columna: str) -> str:
    if df.size == 0:
        return ""
    return pd.to_datetime(df[columna].unique()).strftime(FILE_STRFTIME_DMY)[0]


@st.dialog("Error")
@execute_safely
def error_dialog(message: str):
    st.write(message)


@execute_safely
def centered_title(col, title: str):
    with col.container(height=CENTERED_TITLE_HEIGHT, width=CENTERED_TITLE_WIDTH):
        st.markdown(f"<p style='text-align: center; font-size: 28px;'>{title}</p>", unsafe_allow_html=True)


@execute_safely
def select_box(col, title: str, opt):
    with col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
        return st.selectbox(title, opt, index=None, placeholder=PLACEHOLDER)