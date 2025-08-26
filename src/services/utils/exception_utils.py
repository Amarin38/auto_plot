import traceback
import functools
import logging

from config.dataclasses import TextColors

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

                    logging.error(f"""{TextColors.T_GRAY}--------------------------------------------------------------------------{TextColors.RESET} [{TextColors.T_RED}EXCEPTION{TextColors.RESET}] {TextColors.T_GRAY}--------------------------------------------------------------------------{TextColors.RESET}
                             Exception: {TextColors.ITALIC}{TextColors.T_WHITE}{TextColors.B_RED}{type(e).__name__}{TextColors.RESET}: {TextColors.T_WHITE}{TextColors.B_ORANGE}{e}{TextColors.RESET} 
                             On line {TextColors.UNDERLINE}{TextColors.T_RED}{last.lineno}{TextColors.RESET}: {TextColors.T_RED}{last.line}{TextColors.RESET}
                             Method: {TextColors.T_GREEN}{class_name}{TextColors.RESET}().{TextColors.T_YELLOW}{last.name}{TextColors.RESET}(Args: {TextColors.T_BLUE}{args_kwargs}{TextColors.RESET} | Kwargs: {TextColors.T_MAGENTA}{kwargs}{TextColors.RESET})
                             File: {TextColors.ITALIC}{last.filename}{TextColors.RESET }
                             {TextColors.T_GRAY}-----------------------------------------------------------------------------------------------------------------------------------------------------------------{TextColors.RESET}
                                   """)
                
        return wrapper