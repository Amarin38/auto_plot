import matplotlib.pyplot as plt
import pandas as pd
from config.constants import OUT_PATH
from config.constants import COLORS
from visualization.plot_utils import PlotUtils


class AutoDeviationPlotter:
    def __init__(self, file) -> None:
        self.data = pd.read_excel(f"{OUT_PATH}/{file}.xlsx")
    
    def plot(self):
        fig, ax = plt.subplots(1,1, figsize=(48, 20))
        fig.suptitle("Desviaciones por cabecera", fontsize=25, y=0.93)

        media = self.data["MediaDeMedias"].unique()[0]
        y_data = self.data["Desviacion"]*100
        x_data = self.data["Cabecera"]

        bars = ax.bar(x_data, y_data, color=COLORS[9])
        ax.bar_label(bars, fontsize=18)

        ax.tick_params("x", labelsize=15)
        ax.tick_params("y", labelsize=18)
        
        ax.axhline(0, color="black")
        for x in x_data:
            ax.axvline(x, color=COLORS[9])

        ax.set_ylabel("Desviacion en %", fontsize=25)
        PlotUtils._auto_median_line(ax, media, "%")
        
        plt.savefig(f"{OUT_PATH}/Desviacion_por_cabecera.png")
        plt.show()