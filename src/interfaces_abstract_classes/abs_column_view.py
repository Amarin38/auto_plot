import streamlit as st
from abc import ABC, abstractmethod

from src.config.constants import DISTANCE_COLS_SELECT_PLOT, SELECT_BOX_HEIGHT, BAR_PLOT_BOX_HEIGHT, PIE_PLOT_BOX_HEIGHT, PLACEHOLDER
from src.config.enums import CabecerasEnum, RepuestoEnum, IndexTypeEnum


class ColumnView(ABC):
    @abstractmethod
    def show(self) -> None:
        pass


