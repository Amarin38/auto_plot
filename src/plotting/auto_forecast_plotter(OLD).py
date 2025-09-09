import matplotlib.pyplot as plt
import matplotlib.dates as pltdates

from src.services.utils.exception_utils import execute_safely
from src.services.utils.forecast_utils import ForecastUtils

from .plot_utils import PlotUtils
from src.config.dataclasses import PlotConfig
from src.config.constants import OUT_PATH


class AutoForecastPlotter:
    def __init__(self, file: str, directory: str, rows: int, columns: int, 
                 with_zero: str = "con cero", months_to_forecast: int = 6):
        self.file = file
        self.directory = directory
        self.n_rows = rows
        self.n_cols = columns
        self.months_to_forecast = months_to_forecast
        self.with_zero = with_zero
        self._plot_utils = PlotUtils()
        self.plot_config = PlotConfig()

        df_list = ForecastUtils().prepare_data(self.directory, self.with_zero, self.months_to_forecast)
        self.df_tendencia = df_list[0]
        self.df_data = df_list[1]


    @execute_safely
    def create_figure(self):
        fig, axs = plt.subplots(self.n_rows, self.n_cols, figsize=(self.plot_config.FIG_WIDTH, self.plot_config.FIG_HEIGHT), squeeze=False)
       
        fig.subplots_adjust(wspace=self.plot_config.WSPACE, hspace=self.plot_config.HSPACE)
        fig.suptitle(f"Prevision de compras {self.with_zero} a {self.months_to_forecast} meses", fontsize=self.plot_config.SUPTITLE_SIZE, y=self.plot_config.TITLE_POS)

        return fig, axs


    @execute_safely
    def single_plot(self, repuesto):
        fig, axs = self.create_figure()
        ax = axs[0]

        x_data = self.df_data.loc[self.df_data["Repuesto"] == repuesto, "TotalMes"]
        y_data = self.df_data.loc[self.df_data["Repuesto"] == repuesto, "Fecha"]
        
        x_tendencia = self.df_tendencia.loc[self.df_tendencia["Repuesto"] == repuesto, "TendenciaEstacional"]
        y_tendencia = self.df_tendencia.loc[self.df_tendencia["Repuesto"] == repuesto, "Fecha"]
        
        ax.plot(y_data, x_data, color="#2e7d32", marker="o", linestyle="-")
        ax.plot(y_tendencia, x_tendencia, color="#c62828", marker="s", linestyle="--")

        self._plot_utils._auto_annotate_on_line(x_data, y_data, ax, '#2e7d32', self.plot_config.divisor_factor) # type: ignore
        self._plot_utils._auto_annotate_on_line(x_tendencia, y_tendencia, ax, '#c62828', self.plot_config.divisor_factor) # type: ignore

        self._plot_config(ax, repuesto, x_tendencia)
        plt.savefig(f"{OUT_PATH}/{repuesto}.png")
        plt.show()
        plt.close("all")


    @execute_safely
    def plot(self):
        repuestos = iter(tuple(self.df_tendencia["Repuesto"].unique()))
        fig, axs = self.create_figure()

        for ax in axs.flat: 
            rep = next(repuestos, None)
            
            x_data = self.df_data.loc[self.df_data["Repuesto"] == rep, "TotalMes"]
            y_data = self.df_data.loc[self.df_data["Repuesto"] == rep, "Fecha"]
            # y_data = df_data.loc[df_data["Repuesto"] == rep, "FechaCompleta"].tolist() # type: ignore
            # y_data: pd.DatetimeIndex = pd.to_datetime(y_data, format="%Y-%m")

            x_tendencia = self.df_tendencia.loc[self.df_tendencia["Repuesto"] == rep, "TendenciaEstacional"]
            y_tendencia = self.df_tendencia.loc[self.df_tendencia["Repuesto"] == rep, "Fecha"]
            # y_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "FechaCompleta"].tolist() # type: ignore
            # y_tendencia: pd.DatetimeIndex = pd.to_datetime(y_tendencia, format="%Y-%m")
            
            ax.plot(y_data, x_data, color="#2e7d32", marker="o", linestyle="-")
            ax.plot(y_tendencia, x_tendencia, color="#c62828", marker="s", linestyle="--")

            self._plot_utils._auto_annotate_on_line(x_data, y_data, ax, '#2e7d32', self.plot_config.divisor_factor) # type: ignore
            self._plot_utils._auto_annotate_on_line(x_tendencia, y_tendencia, ax, '#c62828', self.plot_config.divisor_factor) # type: ignore

            self._plot_config(ax, rep, x_tendencia) #type: ignore
        plt.savefig(f"{OUT_PATH}/{self.file}.png")
        plt.show()
        plt.close("all")
    

    @execute_safely
    def _plot_config(self, ax, repuesto: str, x_tendencia):
        bbox = dict(boxstyle ="round", fc ="0.8")
        ax.legend(["Consumo temporal","Tendencia de consumo"], fontsize=self.plot_config.LEGEND_SIZE/self.plot_config.DIV_FACTOR, loc=2)
        ax.axhline(0, color="black")
        ax.set_title(repuesto, fontsize=self.plot_config.PLOT_TITLE_SIZE)
        ax.set_ylabel("Consumo", fontsize=self.plot_config.LABEL_SIZE, labelpad=20)

        ax.tick_params("x", labelsize=self.plot_config.X_TICK_SIZE)
        ax.tick_params("y", labelsize=self.plot_config.Y_TICK_SIZE)

        ax.xaxis.set_major_locator(pltdates.DayLocator(interval=90)) # modifica el intervalo de la fecha
        ax.xaxis.set_major_formatter(pltdates.DateFormatter("%Y-%m")) # modifica el formato de la fecha
        
        ax.text(0.995, 
                0.99, 
                f"Tendencia total: {x_tendencia.sum()}", # type: ignore
                transform=ax.transAxes, 
                va="top", 
                ha="right", 
                fontsize=self.plot_config.TEXT_SIZE/self.plot_config.DIV_FACTOR, 
                bbox=bbox)