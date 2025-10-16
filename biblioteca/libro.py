"""
Módulo que define la clase Libro para el sistema de biblioteca.
"""
from datetime import datetime
from typing import Optional


class Libro:
    """
    Representa un libro en la biblioteca.
    
    Attributes:
        isbn (str): Código ISBN único del libro
        titulo (str): Título del libro
        autor (str): Autor del libro
        disponible (bool): Estado de disponibilidad
        fecha_publicacion (Optional[datetime]): Fecha de publicación
    """
    
    def __init__(self, isbn: str, titulo: str, autor: str, 
                 fecha_publicacion: Optional[datetime] = None):
        """
        Inicializa un nuevo libro.
        
        Args:
            isbn: Código ISBN del libro
            titulo: Título del libro
            autor: Autor del libro
            fecha_publicacion: Fecha de publicación (opcional)
            
        Raises:
            ValueError: Si ISBN, título o autor están vacíos
        """
        if not isbn or not isbn.strip():
            raise ValueError("El ISBN no puede estar vacío")
        if not titulo or not titulo.strip():
            raise ValueError("El título no puede estar vacío")
        if not autor or not autor.strip():
            raise ValueError("El autor no puede estar vacío")
            
        self.isbn = isbn.strip()
        self.titulo = titulo.strip()
        self.autor = autor.strip()
        self.disponible = True
        self.fecha_publicacion = fecha_publicacion
    
    def prestar(self) -> bool:
        """
        Marca el libro como prestado.
        
        Returns:
            bool: True si se pudo prestar, False si ya estaba prestado
        """
        if not self.disponible:
            return False
        self.disponible = False
        return True
    
    def devolver(self) -> bool:
        """
        Marca el libro como devuelto.
        
        Returns:
            bool: True si se pudo devolver, False si ya estaba disponible
        """
        if self.disponible:
            return False
        self.disponible = True
        return True
    
    def __str__(self) -> str:
        """Representación en string del libro."""
        estado = "Disponible" if self.disponible else "Prestado"
        return f"{self.titulo} por {self.autor} (ISBN: {self.isbn}) - {estado}"
    
    def __repr__(self) -> str:
        """Representación técnica del libro."""
        return f"Libro(isbn='{self.isbn}', titulo='{self.titulo}', autor='{self.autor}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos libros por su ISBN."""
        if not isinstance(other, Libro):
            return False
        return self.isbn == other.isbn