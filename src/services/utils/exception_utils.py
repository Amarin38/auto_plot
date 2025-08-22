
# TODO ver como implementar
class ExceptionHandler:
    def __init__(self, func, *args, **kwargs) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute_safely(self) -> None:
        try:
            return self.func(self.args, self.kwargs)
        except Exception as e:
            print(f"""
                  Excepción: {e}
                  Falló la funcion: {self.func}(args: {self.args} | kwargs: {self.kwargs})
                """)
            return None