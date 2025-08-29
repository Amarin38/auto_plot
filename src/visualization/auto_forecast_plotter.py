import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates

from services.utils.forecast_utils import ForecastUtils
from services.utils.exception_utils import execute_safely
from config.dataclasses import PlotConfig
from .plot_utils import PlotUtils


class AutoForecastPlotter:
    def __init__(self, file: str, dir: str, rows: int, columns: int, 
                 with_zero: str = "con cero", months_to_forecast: int = 6):
        self.file = file
        self.dir = dir
        self.n_rows = rows
        self.n_cols = columns
        self.months_to_forecast = months_to_forecast
        self.with_zero = with_zero

        self._plot_utils = PlotUtils()

    @execute_safely
    def create_plot(self) -> None:
        df_tendencia, df_data = ForecastUtils()._prepare_data(self.file, self.dir, self.with_zero, self.months_to_forecast) # type:ignore
        self.plot_forecast(df_tendencia, df_data)


    @execute_safely
    def plot_forecast(self, df_tendencia: pd.DataFrame, df_data: pd.DataFrame):
        fig, axs = plt.subplots(self.n_rows, self.n_cols, figsize=(PlotConfig.figure_width, PlotConfig.figure_height), squeeze=False)
       
        fig.subplots_adjust(wspace=PlotConfig.wspace, hspace=PlotConfig.hspace)
        fig.suptitle(f"Prevision de compras {self.with_zero} a {self.months_to_forecast} meses", fontsize=PlotConfig.suptitle_font_size, y=0.94)

        repuestos = iter(tuple(df_tendencia["Repuesto"].unique()))

        try:
            for i in range(axs.shape[0]): 
                for j in range(axs.shape[1]):
                    rep = next(repuestos) # itero en los repuestos
                    
                    x_data = df_data.loc[df_data["Repuesto"] == rep, "TotalMes"]
                    y_data = df_data.loc[df_data["Repuesto"] == rep, "FechaCompleta"].tolist() # type: ignore
                    y_data: pd.DatetimeIndex = pd.to_datetime(y_data, format="%Y-%m")

                    x_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "TendenciaEstacional"]
                    y_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "FechaCompleta"].tolist() # type: ignore
                    y_tendencia: pd.DatetimeIndex = pd.to_datetime(y_tendencia, format="%Y-%m")
                    
                    axs[i,j].plot(y_data, x_data, color="#2e7d32", marker="o", linestyle="-")
                    axs[i,j].plot(y_tendencia, x_tendencia, color="#c62828", marker="s", linestyle="--")
                    
                    self._plot_utils._auto_annotate_on_line(x_data, y_data, axs[i,j], '#2e7d32', PlotConfig.divisor_factor) # type: ignore
                    self._plot_utils._auto_annotate_on_line(x_tendencia, y_tendencia, axs[i,j], '#c62828', PlotConfig.divisor_factor) # type: ignore
                    
                    bbox = dict(boxstyle ="round", fc ="0.8")
                    axs[i,j].legend(["Consumo temporal","Tendencia de consumo"], fontsize=PlotConfig.legend_fonsize/PlotConfig.divisor_factor, loc=2)
                    axs[i,j].axhline(0, color="black")
                    axs[i,j].set_title(rep, fontsize=PlotConfig.plot_title_fontsize)
                    axs[i,j].set_ylabel("Consumo", fontsize=PlotConfig.label_fontsize, labelpad=20)
                    axs[i,j].tick_params("x", labelsize=PlotConfig.x_tick_fontsize)
                    axs[i,j].tick_params("y", labelsize=PlotConfig.y_tick_fontsize)
                    axs[i,j].xaxis.set_major_locator(pltdates.DayLocator(interval=90))
                    axs[i,j].xaxis.set_major_formatter(pltdates.DateFormatter("%Y-%m"))
                    axs[i,j].text(0.995, 
                                  0.99, 
                                  f"Tendencia total: {x_tendencia.sum()}", # type: ignore
                                  transform=axs[i,j].transAxes, 
                                  va="top", 
                                  ha="right", 
                                  fontsize=PlotConfig.text_font_size/PlotConfig.divisor_factor, 
                                  bbox=bbox)
        except StopIteration:
            rep = ""