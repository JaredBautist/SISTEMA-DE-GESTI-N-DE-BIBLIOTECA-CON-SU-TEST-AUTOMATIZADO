"""
Módulo que define la clase Usuario para el sistema de biblioteca.
"""
from typing import List, Optional


class Usuario:
    """
    Representa un usuario de la biblioteca.
    
    Attributes:
        id (str): Identificador único del usuario
        nombre (str): Nombre completo del usuario
        email (Optional[str]): Email del usuario
        libros_prestados (List[str]): Lista de ISBNs de libros prestados
        limite_prestamos (int): Número máximo de préstamos simultáneos
    """
    
    def __init__(self, id: str, nombre: str, email: Optional[str] = None, 
                 limite_prestamos: int = 3):
        """
        Inicializa un nuevo usuario.
        
        Args:
            id: Identificador único del usuario
            nombre: Nombre del usuario
            email: Email del usuario (opcional)
            limite_prestamos: Límite de préstamos simultáneos
            
        Raises:
            ValueError: Si ID o nombre están vacíos, o límite es inválido
        """
        if not id or not id.strip():
            raise ValueError("El ID no puede estar vacío")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if limite_prestamos < 1:
            raise ValueError("El límite de préstamos debe ser al menos 1")
            
        self.id = id.strip()
        self.nombre = nombre.strip()
        self.email = email.strip() if email else None
        self.libros_prestados: List[str] = []
        self.limite_prestamos = limite_prestamos
    
    def puede_prestar(self) -> bool:
        """
        Verifica si el usuario puede tomar más libros prestados.
        
        Returns:
            bool: True si puede prestar más libros
        """
        return len(self.libros_prestados) < self.limite_prestamos
    
    def agregar_prestamo(self, isbn: str) -> bool:
        """
        Agrega un libro a los préstamos del usuario.
        
        Args:
            isbn: ISBN del libro a prestar
            
        Returns:
            bool: True si se agregó exitosamente
            
        Raises:
            ValueError: Si el usuario ya alcanzó el límite o el libro ya está prestado
        """
        if not self.puede_prestar():
            raise ValueError(f"El usuario ha alcanzado el límite de {self.limite_prestamos} préstamos")
        if isbn in self.libros_prestados:
            raise ValueError("El usuario ya tiene este libro prestado")
            
        self.libros_prestados.append(isbn)
        return True
    
    def remover_prestamo(self, isbn: str) -> bool:
        """
        Remueve un libro de los préstamos del usuario.
        
        Args:
            isbn: ISBN del libro a devolver
            
        Returns:
            bool: True si se removió exitosamente
            
        Raises:
            ValueError: Si el libro no está en los préstamos del usuario
        """
        if isbn not in self.libros_prestados:
            raise ValueError("El usuario no tiene este libro prestado")
            
        self.libros_prestados.remove(isbn)
        return True
    
    def numero_prestamos(self) -> int:
        """Retorna el número de libros prestados actualmente."""
        return len(self.libros_prestados)
    
    def __str__(self) -> str:
        """Representación en string del usuario."""
        return f"{self.nombre} (ID: {self.id}) - {self.numero_prestamos()}/{self.limite_prestamos} préstamos"
    
    def __repr__(self) -> str:
        """Representación técnica del usuario."""
        return f"Usuario(id='{self.id}', nombre='{self.nombre}')"
    
    def __eq__(self, other) -> bool:
        """Compara dos usuarios por su ID."""
        if not isinstance(other, Usuario):
            return False
        return self.id == other.id
