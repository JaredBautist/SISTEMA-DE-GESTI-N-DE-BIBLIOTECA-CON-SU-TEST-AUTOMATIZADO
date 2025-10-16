"""
Tests unitarios para la clase Usuario
"""
import pytest
from biblioteca.usuario import Usuario


class TestUsuario:
    """Suite de tests para la clase Usuario"""
    
    def test_crear_usuario_exitoso(self):
        """Test: Crear un usuario con parámetros válidos"""
        usuario = Usuario("U001", "Juan Pérez", "juan@email.com")
        
        assert usuario.id == "U001"
        assert usuario.nombre == "Juan Pérez"
        assert usuario.email == "juan@email.com"
        assert usuario.libros_prestados == []
        assert usuario.limite_prestamos == 3
    
    def test_crear_usuario_sin_email(self):
        """Test: Crear usuario sin email (opcional)"""
        usuario = Usuario("U001", "Juan Pérez")
        
        assert usuario.email is None
    
    def test_crear_usuario_con_limite_personalizado(self):
        """Test: Crear usuario con límite de préstamos personalizado"""
        usuario = Usuario("U001", "Juan Pérez", limite_prestamos=5)
        
        assert usuario.limite_prestamos == 5
    
    def test_crear_usuario_sin_id_falla(self):
        """Test: Crear usuario sin ID debe lanzar ValueError"""
        with pytest.raises(ValueError, match="El ID no puede estar vacío"):
            Usuario("", "Juan Pérez")
    
    def test_crear_usuario_sin_nombre_falla(self):
        """Test: Crear usuario sin nombre debe lanzar ValueError"""
        with pytest.raises(ValueError, match="El nombre no puede estar vacío"):
            Usuario("U001", "")
    
    def test_crear_usuario_limite_invalido_falla(self):
        """Test: Crear usuario con límite inválido debe lanzar ValueError"""
        with pytest.raises(ValueError, match="El límite de préstamos debe ser al menos 1"):
            Usuario("U001", "Juan Pérez", limite_prestamos=0)
    
    def test_usuario_puede_prestar_inicialmente(self):
        """Test: Usuario recién creado puede prestar libros"""
        usuario = Usuario("U001", "Juan Pérez")
        
        assert usuario.puede_prestar() is True
    
    def test_agregar_prestamo_exitoso(self):
        """Test: Agregar un préstamo al usuario"""
        usuario = Usuario("U001", "Juan Pérez")
        
        resultado = usuario.agregar_prestamo("978-3-16-148410-0")
        
        assert resultado is True
        assert "978-3-16-148410-0" in usuario.libros_prestados
        assert usuario.numero_prestamos() == 1
    
    def test_agregar_prestamo_hasta_limite(self):
        """Test: Agregar préstamos hasta alcanzar el límite"""
        usuario = Usuario("U001", "Juan Pérez", limite_prestamos=2)
        
        usuario.agregar_prestamo("ISBN-001")
        usuario.agregar_prestamo("ISBN-002")
        
        assert usuario.numero_prestamos() == 2
        assert not usuario.puede_prestar()
    
    def test_agregar_prestamo_excede_limite_falla(self):
        """Test: Agregar préstamo cuando se excede el límite debe fallar"""
        usuario = Usuario("U001", "Juan Pérez", limite_prestamos=1)
        usuario.agregar_prestamo("ISBN-001")
        
        with pytest.raises(ValueError, match="ha alcanzado el límite"):
            usuario.agregar_prestamo("ISBN-002")
    
    def test_agregar_prestamo_duplicado_falla(self):
        """Test: Agregar el mismo libro dos veces debe fallar"""
        usuario = Usuario("U001", "Juan Pérez")
        usuario.agregar_prestamo("ISBN-001")
        
        with pytest.raises(ValueError, match="ya tiene este libro prestado"):
            usuario.agregar_prestamo("ISBN-001")
    
    def test_remover_prestamo_exitoso(self):
        """Test: Remover un préstamo del usuario"""
        usuario = Usuario("U001", "Juan Pérez")
        usuario.agregar_prestamo("ISBN-001")
        
        resultado = usuario.remover_prestamo("ISBN-001")
        
        assert resultado is True
        assert "ISBN-001" not in usuario.libros_prestados
        assert usuario.numero_prestamos() == 0
    
    def test_remover_prestamo_inexistente_falla(self):
        """Test: Remover un préstamo que no existe debe fallar"""
        usuario = Usuario("U001", "Juan Pérez")
        
        with pytest.raises(ValueError, match="no tiene este libro prestado"):
            usuario.remover_prestamo("ISBN-001")
    
    def test_numero_prestamos(self):
        """Test: Contar número de préstamos del usuario"""
        usuario = Usuario("U001", "Juan Pérez")
        usuario.agregar_prestamo("ISBN-001")
        usuario.agregar_prestamo("ISBN-002")
        
        assert usuario.numero_prestamos() == 2
    
    def test_str_representation(self):
        """Test: Representación en string del usuario"""
        usuario = Usuario("U001", "Juan Pérez")
        usuario.agregar_prestamo("ISBN-001")
        
        str_usuario = str(usuario)
        
        assert "Juan Pérez" in str_usuario
        assert "U001" in str_usuario
        assert "1/3" in str_usuario
    
    def test_igualdad_usuarios_mismo_id(self):
        """Test: Dos usuarios con el mismo ID son iguales"""
        usuario1 = Usuario("U001", "Juan Pérez")
        usuario2 = Usuario("U001", "Otro Nombre")
        
        assert usuario1 == usuario2