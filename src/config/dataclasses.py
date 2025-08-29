from dataclasses import dataclass

@dataclass
class TextColors():
    T_RED = '\033[91m'
    T_LIGHT_RED = '\033[31m'
    T_GREEN = '\033[92m'
    T_LIGHT_GREEN = '\033[32m'
    T_YELLOW = '\033[33m'
    T_BLUE = '\033[94m'
    T_PURPLE = '\033[95m'
    T_CYAN = '\033[96m'
    T_WHITE = '\033[97m'
    T_BLACK = '\033[90m'
    T_MAGENTA = '\033[35m' 
    T_GRAY = '\033[90m'
    T_ORANGE = '\033[38;5;208m'
    T_FUCHSIA = '\033[38;5;170m'
    
    B_RED = '\033[41m'
    B_ORANGE = '\033[48;5;208m'

    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    DIMM = '\033[22m'

    RESET = '\033[0m'


@dataclass
class PlotConfig:
    figure_width: int = 208
    figure_height: int = 70

    text_font_size: int = 18
    suptitle_font_size: int = 40
    plot_title_fontsize: int = 35
    legend_fonsize: int = 20
    label_fontsize: int = 30
    x_tick_fontsize: float = 16.5
    y_tick_fontsize: int = 15
    bar_fontsize: int = 25

    title_position: float = 0.93
    wspace: float = 0.1
    hspace: float = 0.3
    divisor_factor: float = 0.3
    zorder_multiplier: int = 10
    zorder_base: int = 100