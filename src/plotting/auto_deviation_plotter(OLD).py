import pandas as pd

import matplotlib.pyplot as plt

from src.config.constants import OUT_PATH, COLORS
from src.config.dataclasses import PlotConfig
from src.plotting.plot_utils import PlotUtils
from src.services.utils.exception_utils import execute_safely


class AutoDeviationPlotter:
    def __init__(self, file) -> None:
        self.data = pd.read_excel(f"{OUT_PATH}/{file}.xlsx")
        self.plot_config = PlotConfig()
    

    @execute_safely
    def create_figure(self):
        fig, ax = plt.subplots(1,1, figsize=(self.plot_config.FIG_WIDTH, self.plot_config.FIG_HEIGHT))
        fig.suptitle("Desviaciones por cabecera", fontsize=self.plot_config.SUPTITLE_SIZE, y=0.93)
        
        return fig, ax


    @execute_safely
    def plot(self):
        fig, ax = self.create_figure()

        media = self.data["MediaDeMedias"].unique()[0]
        x_data, y_data = (self.data["Cabecera"], self.data["Desviacion"]*100)

        bars = ax.bar(x_data, y_data, color=COLORS[9])
        ax.bar_label(bars, fontsize=self.plot_config.BAR_SIZE)
        
        self._plot_config(ax, x_data, media)

        plt.savefig(f"{OUT_PATH}/Desviacion_por_cabecera.png")
        plt.show()
        plt.close("all")


    @execute_safely
    def _plot_config(self, ax, x_data, media) -> None:
        ax.tick_params("x", labelsize=self.plot_config.X_TICK_SIZE)
        ax.tick_params("y", labelsize=self.plot_config.Y_TICK_SIZE)
        
        ax.axhline(0, color="black")

        for x in x_data:
            ax.axvline(x, color=COLORS[9]) # coloco lineas verticales en cada nombre de cabecera

        ax.set_ylabel("Desviacion en %", fontsize=self.plot_config.LABEL_SIZE)
        PlotUtils._auto_median_line(ax, media, "%")
        