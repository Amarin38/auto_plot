import streamlit as st
from abc import ABC, abstractmethod

from src.config.constants import DISTANCE_COLS, SELECT_BOX_HEIGHT, PLOT_BOX_HEIGHT, PIE_PLOT_BOX_HEIGHT, PLACEHOLDER
from src.config.enums import CabecerasEnum, RepuestoEnum, IndexTypeEnum


class ColumnView(ABC):
    def __init__(self):
        self.figs = None
        self.col1, self.col2 = st.columns(DISTANCE_COLS)


    @abstractmethod
    def show(self) -> None:
        pass

    def container_select(self):
        return self.col1.container(height=SELECT_BOX_HEIGHT)

    def container_plot(self):
        return self.col2.container(height=PLOT_BOX_HEIGHT)

    def container_pie(self):
        return self.col2.container(height=PIE_PLOT_BOX_HEIGHT)
