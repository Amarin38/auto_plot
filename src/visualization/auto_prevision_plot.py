import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates

from src.config.constants import MAIN_PATH
from src.services import ArreglarListadoExistencias, UpdateListadoExistencias, DeleteListadoExistencias
from src.services import PrevisionCompraSinCero, PrevisionCompraConCero

class AutoPrevisionPlot:
    def __init__(self, nombre_archivo_nuevo: str, carpeta_datos: str, filas: int, columnas: int, con_cero: bool, 
                 tamaño_letra: float, ancho: int = 60, largo: int = 60, meses_en_adelante: int = 6):
        self.nombre_archivo = nombre_archivo_nuevo
        self.carpeta_datos = carpeta_datos
        self.meses_en_adelante = meses_en_adelante
        self.x1 = filas
        self.x2 = columnas
        self._con_cero = con_cero

        self._arreglar = ArreglarListadoExistencias(self.nombre_archivo, self.carpeta_datos)
        self._update = UpdateListadoExistencias(self.nombre_archivo, self.carpeta_datos)
        self._delete = DeleteListadoExistencias(self.nombre_archivo)
        
        if self._con_cero:
            self._prevision = PrevisionCompraConCero(self.nombre_archivo, self.meses_en_adelante)
        else:
            self._prevision = PrevisionCompraSinCero(self.nombre_archivo, self.meses_en_adelante)
            

        self.divisor = 0.3*self.x2
        self.tamaño_letra = tamaño_letra
        self.ancho = ancho
        self.largo = largo


    def graficar(self) -> None:
        """
        ### Grafica la prevision de consumo.
        """

        self._arreglar.arreglar_listado()
        self._prevision.calcular_prevision_compra()

        # ------------- Graficos ---------------
        fig, axs = plt.subplots(self.x1, self.x2, figsize=(self.ancho, self.largo), squeeze=False)
        fig.subplots_adjust(wspace=0.10, hspace=0.15)

        if self._con_cero:
            df_tendencia = pd.read_excel(f"{MAIN_PATH}/out/tendencia-ConCero.xlsx")
            df_data = pd.read_excel(f"{MAIN_PATH}/out/data-ConCero.xlsx")
            fig.suptitle(f"Prevision de compras con cero a {self.meses_en_adelante} meses", fontsize=30, y=0.94)
        else:
            df_tendencia = pd.read_excel(f"{MAIN_PATH}/out/tendencia-SinCero.xlsx")
            df_data = pd.read_excel(f"{MAIN_PATH}/out/data-SinCero.xlsx")
            fig.suptitle(f"Prevision de compras sin cero a {self.meses_en_adelante} meses", fontsize=30, y=0.94)

        repuestos = iter(tuple(df_tendencia["Repuesto"].unique()))

        # ------------------------ Cargo los graficos recursivamente ---------------------------
        try:
            for i in range(axs.shape[0]): 
                for j in range(axs.shape[1]):
                    rep = next(repuestos) # itero en los repuestos
                    
                    x_data = df_data.loc[df_data["Repuesto"] == rep, "TotalMes"]
                    y_data = df_data.loc[df_data["Repuesto"] == rep, "FechaCompleta"].tolist() # type: ignore
                    y_data: pd.DatetimeIndex = pd.to_datetime(y_data, format="%Y-%m")

                    if self._con_cero:
                        x_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "TendenciaEstacionalConCero"]
                    else:
                        x_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "TendenciaEstacionalSinCero"]

                    y_tendencia = df_tendencia.loc[df_tendencia["Repuesto"] == rep, "FechaCompleta"].tolist() # type: ignore
                    y_tendencia: pd.DatetimeIndex = pd.to_datetime(y_tendencia, format="%Y-%m")
                    
                    axs[i,j].plot(y_data, x_data, color="#2e7d32", marker="o", linestyle="-")
                    axs[i,j].plot(y_tendencia, x_tendencia, color="#c62828", marker="s", linestyle="--")
                    
                    _PlotUtils._auto_annotate_on_line(x_data, y_data, axs[i,j], '#2e7d32', self.divisor) # type: ignore
                    _PlotUtils._auto_annotate_on_line(x_tendencia, y_tendencia, axs[i,j], '#c62828', self.divisor) # type: ignore
                    
                    bbox = dict(boxstyle ="round", fc ="0.8")
                    axs[i,j].legend(["Consumo temporal","Tendencia de consumo"], fontsize=20/self.divisor, loc=2)
                    axs[i,j].axhline(0, color="black")
                    axs[i,j].set_title(rep, fontsize=16)
                    axs[i,j].set_ylabel("Consumo", fontsize=20, labelpad=20)
                    axs[i,j].tick_params("x", labelsize=11.25)
                    axs[i,j].tick_params("y", labelsize=15)
                    axs[i,j].xaxis.set_major_locator(pltdates.DayLocator(interval=90))
                    axs[i,j].xaxis.set_major_formatter(pltdates.DateFormatter("%Y-%m"))
                    axs[i,j].text(0.995, 0.99, f"Tendencia total: {x_tendencia.sum()}", transform=axs[i,j].transAxes, va="top", ha="right", fontsize=18/self.divisor, bbox=bbox) # type: ignore
        except StopIteration:
            rep = ""