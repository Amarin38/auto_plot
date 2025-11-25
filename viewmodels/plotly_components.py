from typing import List, Dict, Optional

from config.constants import COLORS
from utils.exception_utils import execute_safely


class HoverComponents:
    def __init__(self):
        ...

    @execute_safely
    def hover_junto(self, fig):
        fig.update_layout(
            hovermode="x unified",  # 🔹 muestra ambos hovers juntos
            hoverlabel=dict(
                bgcolor="#0E1117",  # color de fondo
                bordercolor="black",
                font_size=14.5,  # 🔹 aumenta el tamaño del texto
                font_family="Arial",
                namelength=-1
            ),
        )

    @execute_safely
    def hover_x(self, fig):
        fig.update_layout(
            hovermode="x",  # 🔹 muestra ambos hovers juntos
            hoverlabel=dict(
                bgcolor="#0E1117",  # color de fondo
                bordercolor="black",
                font_size=14.5,  # 🔹 aumenta el tamaño del texto
                font_family="Arial",
                namelength=-1
            ),
        )

    @execute_safely
    def hover_y(self, fig):
        fig.update_layout(
            hovermode="y",  # 🔹 muestra ambos hovers juntos
            hoverlabel=dict(
                bgcolor="#0E1117",  # color de fondo
                bordercolor="black",
                font_size=14.5,  # 🔹 aumenta el tamaño del texto
                font_family="Arial",
                namelength=-1
            ),
        )


class LegendComponents:
    def __init__(self):
        ...

    @execute_safely
    def top_right_legend(self, fig):
        fig.update_layout(
            autosize=True,
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


class SliderComponents:
    def __init__(self):
        ...

    @execute_safely
    def range_slider(self, fig):
        fig.update_layout(
            xaxis=dict(
                range=["2024-06-01", "2026-12-01"],
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


class DropDownComponents:
    def __init__(self):
        ...

    @execute_safely
    def dropdown(self, fig, buttons: List[Dict]):
        fig.update_layout(
            updatemenus=[
                dict(
                    type="dropdown",
                    direction="down",
                    x=0.5,
                    y=1.15,
                    xanchor="center",
                    yanchor="top",
                    font=dict(color="white", size=14),
                    active=0,
                    bgcolor=COLORS[-1],
                    pad=dict(l=1, r=800, t=12, b=5),
                    showactive=True,

                    buttons=buttons
                )
            ]
        )


class DefaultUpdateLayoutComponents:
    def __init__(self):
        ...

    @execute_safely
    def update_layout(self, fig, title: str, x_title: str = None, y_title: str = None, height: Optional[int] = 500,
                      width: Optional[int] = 500):
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
