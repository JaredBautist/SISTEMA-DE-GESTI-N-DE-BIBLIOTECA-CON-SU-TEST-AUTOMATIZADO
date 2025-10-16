class BibliotecaError(Exception):
    """Base para errores del dominio Biblioteca."""


class LibroNoDisponibleError(BibliotecaError):
    pass


class UsuarioNoExisteError(BibliotecaError):
    pass


class LibroNoExisteError(BibliotecaError):
    pass


class PrestamoNoExisteError(BibliotecaError):
    pass


class PrestamoDuplicadoError(BibliotecaError):
    pass
