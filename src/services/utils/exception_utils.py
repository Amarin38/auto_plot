from config.dataclasses import TextColors

# TODO ver como implementar
class ExceptionHandler:
    @staticmethod
    def execute_safely(func, *args, **kwargs) -> None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"""
Excepción: {TextColors.RED}{e}{TextColors.RESET}
Falló la funcion: {TextColors.GREEN}{func.__self__.__class__.__name__}(){TextColors.RESET}.{TextColors.YELLOW}{func.__name__}{TextColors.RESET}(args: {TextColors.BLUE}{args}{TextColors.RESET} | kwargs: {TextColors.MAGENTA}{kwargs}{TextColors.RESET})
                  """)
            return None