import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates

from numpy import ndarray
from typing import List, Dict, Union

from plot_backend.prevision_compra import CalcularPrevisionCompra
from plot_backend.indice_consumo import IndicePorCoche, IndicePorMotor, _IndiceUtils
from plot_backend.arreglar.arreglar_listado_existencias import ArreglarListadoExistencias
from plot_backend.utils.utils_listado_existencias import UpdateListadoExistencias, DeleteListadoExistencias
from src.config.constants import COLORES, MAIN_PATH

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
        
        self._prevision = CalcularPrevisionCompra(self.nombre_archivo, self._con_cero, self.meses_en_adelante)


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
            df_tendencia = pd.read_excel(f"{MAIN_PATH}/excel/tendencia-ConCero.xlsx")
            df_data = pd.read_excel(f"{MAIN_PATH}/excel/data-ConCero.xlsx")
            fig.suptitle(f"Prevision de compras con cero a {self.meses_en_adelante} meses", fontsize=30, y=0.94)
        else:
            df_tendencia = pd.read_excel(f"{MAIN_PATH}/excel/tendencia-SinCero.xlsx")
            df_data = pd.read_excel(f"{MAIN_PATH}/excel/data-SinCero.xlsx")
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


class AutoIndicePlot:
    def __init__(self, nombre_archivo_nuevo: str, carpeta_datos: str, filas: int, columnas: int, 
                 tamaño_letra: int = 15, ancho: int = 60, largo: int = 60) -> None:
        self.nombre_archivo = nombre_archivo_nuevo
        self.carpeta_datos = carpeta_datos
        self.x1 = filas
        self.x2 = columnas

        self._arreglar = ArreglarListadoExistencias(self.nombre_archivo, self.carpeta_datos)
        self._update = UpdateListadoExistencias(self.nombre_archivo, self.carpeta_datos)
        self._delete = DeleteListadoExistencias(self.nombre_archivo)

        self.divisor = 0.3*self.x2
        self.tamaño_letra = tamaño_letra
        self.ancho = ancho
        self.largo = largo


    def graficar(self, stacked_barplot: bool, con_motor: bool) -> None:
        """
        ### Grafica el índice de consumo.\n
        #### Args:\n
            stacked_barplot (bool):\n
                - True -> un solo grafico apilado\n
                - False -> multiples graficos\n
            con_motor (bool): \n
                - True -> indice con motores totales por cabecera\n
                - False -> indice con coches totales por cabecera\n
        #### Returns:
            None
        """
        
        self._arreglar.arreglar_listado()
        
        if con_motor:
            df_rows = self._update.update_rows_by_dict(self.nombre_archivo, "motores")
            df_rows.to_excel(f"{MAIN_PATH}/excel/{self.nombre_archivo}-S.xlsx")
            lista_indice: List[Union[pd.DataFrame, str]] = IndicePorMotor(self.nombre_archivo).calcular() # calculo el indice por motores
        else:
            lista_indice: List[Union[pd.DataFrame, str]] = IndicePorCoche(self.nombre_archivo).calcular() # calculo el indice por coche
        
        df_indices_consumo: Union[pd.DataFrame, str] = lista_indice[0]

        # ---------------------------- GRAFICO ---------------------------- #
        repuestos = iter(tuple(df_indices_consumo["Repuesto"].unique())) # type: ignore
        
        if stacked_barplot:
            fig, ax = plt.subplots(figsize=(self.ancho, self.largo), squeeze=False)
            
            y_dict_consumo: Dict[str, int] = {}
            
            for rep in repuestos:
                rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                x_cabecera: List[str] = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                y_dict_consumo.update({
                    rep:df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                    })

            for repuesto, y_consumo in y_dict_consumo.items():  # type: ignore
                zorder: int = round((100/max(y_consumo))*10, 0) # type: ignore
            
                try:
                    color = next(COLORES) # itero sobre los colores
                except StopIteration:
                    pass
                
                bars = ax.bar(x_cabecera, y_consumo, label=repuesto, color=color, zorder=zorder) # type: ignore
                
                ax.bar_label(bars, fontsize=15) # type: ignore
            
            # --- Configuración --- #
            ax.legend(loc="upper right", fontsize=18) # type: ignore
            ax.tick_params("x", labelsize=11.5/self.divisor) # type: ignore
            ax.tick_params("y", labelsize=15) # type: ignore

        else:
            fig, axs = plt.subplots(self.x1, self.x2, figsize=(self.ancho, self.largo), squeeze=False)
            
            for i in range(axs.shape[0]):
                for j in range(axs.shape[1]):
                    try:
                        rep = next(repuestos)
                        color = next(COLORES)
                    except StopIteration:
                        rep = ""
                    
                    rep_comparado: bool = df_indices_consumo["Repuesto"] == rep # type: ignore

                    x_cabecera: ndarray = df_indices_consumo.loc[rep_comparado, "Cabecera"] # type: ignore
                    y_consumo: ndarray = df_indices_consumo.loc[rep_comparado, "IndiceConsumo"] # type: ignore
                    
                    bars = axs[i,j].bar(x_cabecera, y_consumo, color=color) # type: ignore
                    axs[i,j].bar_label(bars, fontsize=17)

                    media_con_cero = _IndiceUtils._media_consumo(y_consumo.tolist(), con_cero=True)
                    axs[i,j].axhline(y=media_con_cero, linestyle="--", color="#618B4A")
                    axs[i,j].text(x=1.01, y=media_con_cero, s=f"{media_con_cero}", color="black", va="center", transform=axs[i,j].get_yaxis_transform(), fontsize=self.tamaño_letra*2)

                    media_sin_cero = _IndiceUtils._media_consumo(y_consumo.tolist(), con_cero=False)
                    axs[i,j].axhline(y=media_sin_cero, linestyle="--", color="#922D50")
                    axs[i,j].text(x=1.01, y=media_sin_cero, s=f"{media_sin_cero}", color="black", va="center", transform=axs[i,j].get_yaxis_transform(), fontsize=self.tamaño_letra*2)

                    axs[i,j].legend(["Media con cero","Media sin cero"], fontsize=self.tamaño_letra, loc=1)
                    axs[i,j].axhline(0, color="black")
                    axs[i,j].set_title(rep, fontsize=25)
                    axs[i,j].set_ylabel("Consumo", fontsize=20, labelpad=20)

                    axs[i,j].tick_params("x", labelsize=self.tamaño_letra)
                    axs[i,j].tick_params("y", labelsize=self.tamaño_letra*2)

        fig.suptitle(f"Indice {lista_indice[1]}", fontsize=40, y=0.93)
        fig.subplots_adjust(wspace=0.10, hspace=0.3)


class _PlotUtils:
    @staticmethod
    def _auto_annotate_on_line(x_data: List[str], y_data: List[str], axs, color: str, divisor: float) -> None:
        """
            ### Returns an axs.annotate object with the data and color entered
            ### displayed above the offset points.\n
            #### Args:\n
                x_data (List[str]) -> Data from the x axis\n
                y_data (List[str]) -> Data from the y axis\n
                axs (plt.subplots) -> The ax selected for annotation\n
                color (str) -> The color used in the line\n
                divisor (float) -> Number to divide the size number on the line
            #### Returns:\n
                axs.annotate 
        """

        for y, x in zip(y_data, x_data): # labels tendencia
                    axs.annotate(
                        f"{x:.0f}",      
                        xy=(y, x), # type: ignore
                        xytext=(0, 5),   
                        textcoords='offset points',
                        ha='center',
                        va='bottom',
                        fontsize=15/divisor,
                        color=color
                    )

    @staticmethod
    def _auto_reshape_2D(axs, x1: int, x2: int) -> None:
        """
        Automatically reshapes the plot if its 1D.
        
        if axs.ndim == 1:
            axs = auto_reshape_2D(axs, x1, x2)

        """
        if x1 == 1:
            axs = axs.reshape(-1, x2)
        elif x2 == 1:
            axs =  axs.reshape(x1, -1)
        else:
            axs =  axs.reshape(-1, -1)
        return axs
    
