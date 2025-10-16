"""
Módulo que define la clase Prestamo para el sistema de biblioteca.
"""
from datetime import datetime, timedelta
from typing import Optional


class Prestamo:
    """
    Representa un préstamo de libro en la biblioteca.
    
    Attributes:
        id (str): Identificador único del préstamo
        isbn_libro (str): ISBN del libro prestado
        id_usuario (str): ID del usuario que realiza el préstamo
        fecha_prestamo (datetime): Fecha en que se realizó el préstamo
        fecha_devolucion (Optional[datetime]): Fecha de devolución del libro
        dias_prestamo (int): Días permitidos para el préstamo
    """
    
    def __init__(self, id: str, isbn_libro: str, id_usuario: str, 
                 dias_prestamo: int = 14):
        """
        Inicializa un nuevo préstamo.
        
        Args:
            id: Identificador único del préstamo
            isbn_libro: ISBN del libro
            id_usuario: ID del usuario
            dias_prestamo: Días permitidos para el préstamo
            
        Raises:
            ValueError: Si algún parámetro es inválido
        """
        if not id or not id.strip():
            raise ValueError("El ID del préstamo no puede estar vacío")
        if not isbn_libro or not isbn_libro.strip():
            raise ValueError("El ISBN del libro no puede estar vacío")
        if not id_usuario or not id_usuario.strip():
            raise ValueError("El ID del usuario no puede estar vacío")
        if dias_prestamo < 1:
            raise ValueError("Los días de préstamo deben ser al menos 1")
            
        self.id = id.strip()
        self.isbn_libro = isbn_libro.strip()
        self.id_usuario = id_usuario.strip()
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion: Optional[datetime] = None
        self.dias_prestamo = dias_prestamo
    
    def esta_activo(self) -> bool:
        """
        Verifica si el préstamo está activo.
        
        Returns:
            bool: True si el préstamo no ha sido devuelto
        """
        return self.fecha_devolucion is None
    
    def devolver(self) -> bool:
        """
        Registra la devolución del libro.
        
        Returns:
            bool: True si se devolvió exitosamente
            
        Raises:
            ValueError: Si el libro ya fue devuelto
        """
        if not self.esta_activo():
            raise ValueError("Este préstamo ya fue devuelto")
            
        self.fecha_devolucion = datetime.now()
        return True
    
    def dias_transcurridos(self) -> int:
        """
        Calcula los días transcurridos desde el préstamo.
        
        Returns:
            int: Número de días transcurridos
        """
        fecha_referencia = self.fecha_devolucion if self.fecha_devolucion else datetime.now()
        delta = fecha_referencia - self.fecha_prestamo
        return delta.days
    
    def esta_vencido(self) -> bool:
        """
        Verifica si el préstamo está vencido.
        
        Returns:
            bool: True si el préstamo superó los días permitidos
        """
        if not self.esta_activo():
            return False
        return self.dias_transcurridos() > self.dias_prestamo
    
    def dias_restantes(self) -> int:
        """
        Calcula los días restantes del préstamo.
        
        Returns:
            int: Días restantes (negativo si está vencido)
        """
        if not self.esta_activo():
            return 0
        return self.dias_prestamo - self.dias_transcurridos()
    
    def __str__(self) -> str:
        """Representación en string del préstamo."""
        estado = "Activo" if self.esta_activo() else "Devuelto"
        return f"Préstamo {self.id}: Libro {self.isbn_libro} - Usuario {self.id_usuario} ({estado})"
    
    def __repr__(self) -> str:
        """Representación técnica del préstamo."""
        return f"Prestamo(id='{self.id}', isbn_libro='{self.isbn_libro}', id_usuario='{self.id_usuario}')"