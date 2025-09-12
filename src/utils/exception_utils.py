import traceback
import functools
import logging

from src.config.constants import T_GRAY, T_WHITE, T_RED, T_MAGENTA, T_YELLOW, T_BLUE, T_GREEN
from src.config.constants import B_ORANGE, B_RED
from src.config.constants import UNDERLINE, ITALIC, RESET


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

                    logging.error(f"""{T_GRAY}--------------------------------------------------------------------------{RESET} [{T_RED}EXCEPTION{RESET}] {T_GRAY}--------------------------------------------------------------------------{RESET}
                             Exception: {ITALIC}{T_WHITE}{B_RED}{type(e).__name__}{RESET}: {T_WHITE}{B_ORANGE}{e}{RESET} 
                             On line {UNDERLINE}{T_RED}{last.lineno}{RESET}: {T_RED}{last.line}{RESET}
                             Method: {T_GREEN}{class_name}{RESET}().{T_YELLOW}{last.name}{RESET}(Args: {T_BLUE}{args_kwargs}{RESET} | Kwargs: {T_MAGENTA}{kwargs}{RESET})
                             File: {ITALIC}{last.filename}{RESET }
                             {T_GRAY}-----------------------------------------------------------------------------------------------------------------------------------------------------------------{RESET}
                                   """)
        return wrapper