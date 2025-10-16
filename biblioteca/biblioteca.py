"""
Módulo que define la clase Biblioteca - sistema principal de gestión.
"""
from typing import Dict, List, Optional
from datetime import datetime
from .libro import Libro
from .usuario import Usuario
from .prestamo import Prestamo


class Biblioteca:
    """
    Sistema principal de gestión de biblioteca.
    
    Attributes:
        nombre (str): Nombre de la biblioteca
        catalogo (Dict[str, Libro]): Catálogo de libros indexados por ISBN
        usuarios (Dict[str, Usuario]): Usuarios registrados indexados por ID
        prestamos (Dict[str, Prestamo]): Préstamos indexados por ID
    """
    
    def __init__(self, nombre: str = "Biblioteca Central"):
        """
        Inicializa una nueva biblioteca.
        
        Args:
            nombre: Nombre de la biblioteca
        """
        self.nombre = nombre
        self.catalogo: Dict[str, Libro] = {}
        self.usuarios: Dict[str, Usuario] = {}
        self.prestamos: Dict[str, Prestamo] = {}
        self._contador_prestamos = 0
    
    # ==================== GESTIÓN DE LIBROS ====================
    
    def agregar_libro(self, libro: Libro) -> bool:
        """
        Agrega un libro al catálogo.
        
        Args:
            libro: Objeto Libro a agregar
            
        Returns:
            bool: True si se agregó exitosamente
            
        Raises:
            ValueError: Si el libro ya existe en el catálogo
        """
        if libro.isbn in self.catalogo:
            raise ValueError(f"El libro con ISBN {libro.isbn} ya existe en el catálogo")
        
        self.catalogo[libro.isbn] = libro
        return True
    
    def buscar_libro_por_isbn(self, isbn: str) -> Optional[Libro]:
        """
        Busca un libro por su ISBN.
        
        Args:
            isbn: ISBN del libro a buscar
            
        Returns:
            Optional[Libro]: El libro si existe, None en caso contrario
        """
        return self.catalogo.get(isbn)
    
    def buscar_libros_por_titulo(self, titulo: str) -> List[Libro]:
        """
        Busca libros por título (búsqueda parcial, case-insensitive).
        
        Args:
            titulo: Título o parte del título a buscar
            
        Returns:
            List[Libro]: Lista de libros que coinciden
        """
        titulo_lower = titulo.lower()
        return [
            libro for libro in self.catalogo.values()
            if titulo_lower in libro.titulo.lower()
        ]
    
    def buscar_libros_por_autor(self, autor: str) -> List[Libro]:
        """
        Busca libros por autor (búsqueda parcial, case-insensitive).
        
        Args:
            autor: Autor o parte del nombre a buscar
            
        Returns:
            List[Libro]: Lista de libros que coinciden
        """
        autor_lower = autor.lower()
        return [
            libro for libro in self.catalogo.values()
            if autor_lower in libro.autor.lower()
        ]
    
    def libros_disponibles(self) -> List[Libro]:
        """
        Retorna todos los libros disponibles.
        
        Returns:
            List[Libro]: Lista de libros disponibles
        """
        return [libro for libro in self.catalogo.values() if libro.disponible]
    
    def total_libros(self) -> int:
        """Retorna el número total de libros en el catálogo."""
        return len(self.catalogo)
    
    # ==================== GESTIÓN DE USUARIOS ====================
    
    def registrar_usuario(self, usuario: Usuario) -> bool:
        """
        Registra un nuevo usuario en la biblioteca.
        
        Args:
            usuario: Objeto Usuario a registrar
            
        Returns:
            bool: True si se registró exitosamente
            
        Raises:
            ValueError: Si el usuario ya existe
        """
        if usuario.id in self.usuarios:
            raise ValueError(f"El usuario con ID {usuario.id} ya está registrado")
        
        self.usuarios[usuario.id] = usuario
        return True
    
    def buscar_usuario(self, id_usuario: str) -> Optional[Usuario]:
        """
        Busca un usuario por su ID.
        
        Args:
            id_usuario: ID del usuario a buscar
            
        Returns:
            Optional[Usuario]: El usuario si existe, None en caso contrario
        """
        return self.usuarios.get(id_usuario)
    
    def total_usuarios(self) -> int:
        """Retorna el número total de usuarios registrados."""
        return len(self.usuarios)
    
    # ==================== GESTIÓN DE PRÉSTAMOS ====================
    
    def prestar_libro(self, isbn: str, id_usuario: str, dias_prestamo: int = 14) -> Prestamo:
        """
        Realiza un préstamo de libro a un usuario.
        
        Args:
            isbn: ISBN del libro a prestar
            id_usuario: ID del usuario que solicita el préstamo
            dias_prestamo: Días de duración del préstamo
            
        Returns:
            Prestamo: Objeto del préstamo creado
            
        Raises:
            ValueError: Si el libro no existe, no está disponible,
                       el usuario no existe o alcanzó el límite
        """
        # Validar libro
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro:
            raise ValueError(f"El libro con ISBN {isbn} no existe en el catálogo")
        if not libro.disponible:
            raise ValueError(f"El libro '{libro.titulo}' no está disponible")
        
        # Validar usuario
        usuario = self.buscar_usuario(id_usuario)
        if not usuario:
            raise ValueError(f"El usuario con ID {id_usuario} no está registrado")
        if not usuario.puede_prestar():
            raise ValueError(f"El usuario ha alcanzado el límite de {usuario.limite_prestamos} préstamos")
        
        # Crear préstamo
        self._contador_prestamos += 1
        id_prestamo = f"PREST-{self._contador_prestamos:05d}"
        prestamo = Prestamo(id_prestamo, isbn, id_usuario, dias_prestamo)
        
        # Actualizar estados
        libro.prestar()
        usuario.agregar_prestamo(isbn)
        self.prestamos[id_prestamo] = prestamo
        
        return prestamo
    
    def devolver_libro(self, isbn: str, id_usuario: str) -> bool:
        """
        Procesa la devolución de un libro.
        
        Args:
            isbn: ISBN del libro a devolver
            id_usuario: ID del usuario que devuelve el libro
            
        Returns:
            bool: True si se devolvió exitosamente
            
        Raises:
            ValueError: Si el préstamo no existe o ya fue devuelto
        """
        # Buscar préstamo activo
        prestamo = self._buscar_prestamo_activo(isbn, id_usuario)
        if not prestamo:
            raise ValueError(f"No existe un préstamo activo para el libro {isbn} y usuario {id_usuario}")
        
        # Buscar libro y usuario
        libro = self.buscar_libro_por_isbn(isbn)
        usuario = self.buscar_usuario(id_usuario)
        
        if not libro or not usuario:
            raise ValueError("Error en los datos del préstamo")
        
        # Procesar devolución
        prestamo.devolver()
        libro.devolver()
        usuario.remover_prestamo(isbn)
        
        return True
    
    def _buscar_prestamo_activo(self, isbn: str, id_usuario: str) -> Optional[Prestamo]:
        """
        Busca un préstamo activo para un libro y usuario específicos.
        
        Args:
            isbn: ISBN del libro
            id_usuario: ID del usuario
            
        Returns:
            Optional[Prestamo]: El préstamo si existe y está activo
        """
        for prestamo in self.prestamos.values():
            if (prestamo.isbn_libro == isbn and 
                prestamo.id_usuario == id_usuario and 
                prestamo.esta_activo()):
                return prestamo
        return None
    
    def prestamos_activos(self) -> List[Prestamo]:
        """
        Retorna todos los préstamos activos.
        
        Returns:
            List[Prestamo]: Lista de préstamos activos
        """
        return [p for p in self.prestamos.values() if p.esta_activo()]
    
    def prestamos_vencidos(self) -> List[Prestamo]:
        """
        Retorna todos los préstamos vencidos.
        
        Returns:
            List[Prestamo]: Lista de préstamos vencidos
        """
        return [p for p in self.prestamos.values() if p.esta_vencido()]
    
    def prestamos_usuario(self, id_usuario: str) -> List[Prestamo]:
        """
        Retorna todos los préstamos de un usuario.
        
        Args:
            id_usuario: ID del usuario
            
        Returns:
            List[Prestamo]: Lista de préstamos del usuario
        """
        return [p for p in self.prestamos.values() if p.id_usuario == id_usuario]
    
    def total_prestamos(self) -> int:
        """Retorna el número total de préstamos registrados."""
        return len(self.prestamos)
    
    # ==================== ESTADÍSTICAS ====================
    
    def estadisticas(self) -> Dict:
        """
        Genera estadísticas de la biblioteca.
        
        Returns:
            Dict: Diccionario con estadísticas
        """
        return {
            'total_libros': self.total_libros(),
            'libros_disponibles': len(self.libros_disponibles()),
            'libros_prestados': self.total_libros() - len(self.libros_disponibles()),
            'total_usuarios': self.total_usuarios(),
            'total_prestamos': self.total_prestamos(),
            'prestamos_activos': len(self.prestamos_activos()),
            'prestamos_vencidos': len(self.prestamos_vencidos())
        }
    
    def __str__(self) -> str:
        """Representación en string de la biblioteca."""
        return f"{self.nombre} - {self.total_libros()} libros, {self.total_usuarios()} usuarios"