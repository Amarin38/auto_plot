from dataclasses import dataclass
from typing import Literal

@dataclass
class PlotConfig:
    figure_width: Literal[70] = 70
    figure_height: Literal[70] = 70

    text_font_size: Literal[15] = 15
    suptitle_font_size: Literal[40] = 40
    plot_title_fontsize: Literal[25] = 25
    legend_fonsize: Literal[20] = 20
    label_fontsize: Literal[20] = 20
    x_tick_fontsize: float = 11.25
    y_tick_fontsize: Literal[15] = 15

    wspace: float = 0.1
    hspace: float = 0.3
    divisor_factor: float = 0.3
    zorder_multiplier: Literal[10] = 10
    zorder_base: Literal[100] = 100