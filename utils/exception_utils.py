import traceback
import functools
import logging

from config.enums_colors import TextModsEnum, BackgroundColorsEnum, ForegroundColorsEnum


logging.basicConfig(
     level=logging.ERROR,
     format="%(asctime)s | %(levelname)s --> %(message)s ",
     datefmt="%Y/%m/%d %H:%M"
)


def execute_safely(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tb = traceback.TracebackException.from_exception(e, capture_locals=True)
                last_frame = list(tb.stack)

                for last in last_frame:
                    class_name = str(last).split("\\")[-1].split(".")[0]
                    args_kwargs = last.locals.popitem() # type:ignore

                    logging.error(f"""{ForegroundColorsEnum.T_GRAY}--------------------------------------------------------------------------{TextModsEnum.RESET} [{ForegroundColorsEnum.T_RED}EXCEPTION{TextModsEnum.RESET}] {ForegroundColorsEnum.T_GRAY}--------------------------------------------------------------------------{TextModsEnum.RESET}
                             Exception: {TextModsEnum.ITALIC}{ForegroundColorsEnum.T_WHITE}{BackgroundColorsEnum.B_RED}{type(e).__name__}{TextModsEnum.RESET}: {ForegroundColorsEnum.T_WHITE}{BackgroundColorsEnum.B_ORANGE}{e}{TextModsEnum.RESET} 
                             On line {TextModsEnum.UNDERLINE}{ForegroundColorsEnum.T_RED}{last.lineno}{TextModsEnum.RESET}: {ForegroundColorsEnum.T_RED}{last.line}{TextModsEnum.RESET}
                             Method: {ForegroundColorsEnum.T_GREEN}{class_name}{TextModsEnum.RESET}().{ForegroundColorsEnum.T_YELLOW}{last.name}{TextModsEnum.RESET}(Args: {ForegroundColorsEnum.T_BLUE}{args_kwargs}{TextModsEnum.RESET} | Kwargs: {ForegroundColorsEnum.T_MAGENTA}{kwargs}{TextModsEnum.RESET})
                             File: {TextModsEnum.ITALIC}{last.filename}{TextModsEnum.RESET}
                             {ForegroundColorsEnum.T_GRAY}-----------------------------------------------------------------------------------------------------------------------------------------------------------------{TextModsEnum.RESET}
                                   """)
        return wrapper